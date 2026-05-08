# 安全框架 API（Security Framework API）

openvela 安全框架基于 MiTEE（可信执行环境）提供安全存储、密钥管理和安全支付等能力，遵循 GlobalPlatform（GP）TEE 标准。

本文档涵盖以下内容：

- MiTEE CA 应用级 API 接口（SST 安全存储、三元组、微信/支付宝支付、PIN 码）
- MiTEE Rootkey API 接口
- GP TEE Client API（REE 侧，供 CA 调用）
- GP TEE Internal API（TEE 侧，供 TA 实现使用）

头文件：`frameworks/security/include/` 下的各 CA 头文件（`comsst_ca_api.h` / `triad_ca_api.h` 等），以及 `<sys/boardctl.h>`（Rootkey）、OP-TEE `<tee_client_api.h>`（TEE Client）、`<tee_internal_api.h>`（TEE Internal）。

## openvela 实现说明

- **安全方案双轨并存**：openvela 提供两套可选的安全能力——
    - **基于 MiTEE 的 TEE 方案**（本文主要内容）：面向需要硬件级可信执行环境的场景
    - **Android Keystore 方案**（见"Android Keystore Client API"小节）：移植自 AOSP，面向只需密钥管理与安全存储的轻量场景
- **基于 MiTEE**：openvela 的 TEE 实现，与 OP-TEE 兼容，遵循 GlobalPlatform（GP）规范
- **两侧运行时**：
    - **REE 侧**（Rich Execution Environment）：运行 CA（Client Application），通过 `libteec` 发起 TEE 请求
    - **TEE 侧**（Trusted Execution Environment）：运行 TA（Trusted Application），由 `miteed` 服务器调度
- **通信通道**：CA 与 TA 之间通过 rpmsg socket 进行数据交换
- **API 层次**：
    - 应用级 CA API（位于 `frameworks/security/ca/`）封装常见的安全业务（SST、三元组、支付、PIN）
    - GP TEE Client API（REE 侧）提供 GP 标准的 Context/Session 管理与命令调用
    - GP TEE Internal API（TEE 侧）提供 TA 实现者可调用的内存/对象/加解密能力
- **密钥根**：Rootkey 在工厂阶段一次性写入，运行时不可变，所有派生密钥都从 Rootkey 推导

## 通用安全存储 SST CA API

对安全存储（Secure Storage，SST）分区执行读写操作。实现位于 `frameworks/security/ca/comsst`。

### comsst_data_read

```c
uint32_t comsst_data_read(uint8_t *scope, uint8_t *name, bool is_deletable,
                          uint8_t *buff, uint32_t *out_len);
```

从 SST 分区读取一条数据记录。

**参数**：

- `scope` 命名空间（范围标识），用于区分不同业务。
- `name` 记录名称。
- `is_deletable` 该记录是否允许被用户侧删除。
- `buff` 输出缓冲区，接收读取到的数据。
- `out_len` 输入输出参数，输入为缓冲区大小，输出为实际读取长度。

**返回值**：

成功时返回 `TEE_SUCCESS`（`0`），失败时返回 TEE 错误码。

### comsst_data_write

```c
uint32_t comsst_data_write(uint8_t *scope, uint8_t *name, bool is_deletable,
                           uint8_t *buff, uint32_t len);
```

向 SST 分区写入一条数据记录。

**参数**：

- `scope` 命名空间。
- `name` 记录名称。
- `is_deletable` 该记录是否允许被用户侧删除。
- `buff` 要写入的数据缓冲区。
- `len` 数据长度。

**返回值**：

成功时返回 `TEE_SUCCESS`，失败时返回 TEE 错误码。

### comsst_data_delete

```c
uint32_t comsst_data_delete(uint8_t *scope, uint8_t *name, bool is_deletable);
```

删除 SST 分区中的一条记录。

**参数**：

- `scope` 命名空间。
- `name` 记录名称。
- `is_deletable` 该记录的可删除属性，需与写入时一致。

**返回值**：

成功时返回 `TEE_SUCCESS`，失败时返回 TEE 错误码。

### is_comsst_data_exited

```c
uint32_t is_comsst_data_exited(uint8_t *scope, uint8_t *name, bool is_deletable);
```

查询 SST 分区中是否存在指定记录。

**参数**：

- `scope` 命名空间。
- `name` 记录名称。
- `is_deletable` 可删除属性。

**返回值**：

存在时返回 `TEE_SUCCESS`，不存在时返回对应错误码。

### comsst_data_verify

```c
uint32_t comsst_data_verify(uint8_t *scope, uint8_t *name, bool is_deletable,
                            uint8_t *buff, uint32_t len);
```

比较传入数据与 SST 中已存储数据是否一致。常用于校验应用端持有的副本是否为最新。

**参数**：

- `scope` 命名空间。
- `name` 记录名称。
- `is_deletable` 可删除属性。
- `buff` 待比较的数据。
- `len` 数据长度。

**返回值**：

一致时返回 `TEE_SUCCESS`，不一致或失败时返回错误码。

## 三元组 CA API

对设备三元组中的设备标识（DID）和密钥（Key）执行读写操作。实现位于 `frameworks/security/ca/triad`。

### triad_store_did

```c
int triad_store_did(uint8_t *did, uint16_t len);
```

将设备 DID 写入安全存储。

**参数**：

- `did` DID 缓冲区。
- `len` DID 长度（字节）。

**返回值**：

成功时返回 `0`，失败时返回负值错误码。

### triad_load_did

```c
int triad_load_did(uint8_t *did, uint16_t len);
```

从安全存储读取 DID。

**参数**：

- `did` 输出缓冲区，接收 DID。
- `len` 缓冲区长度。

**返回值**：

成功时返回 `0`，失败时返回负值错误码。

### triad_store_key

```c
int triad_store_key(uint8_t *key, uint16_t len);
```

将设备密钥写入安全存储。

**参数**：

- `key` 密钥缓冲区。
- `len` 密钥长度。

**返回值**：

成功时返回 `0`，失败时返回负值错误码。

### triad_load_key

```c
int triad_load_key(uint8_t *key, uint16_t len);
```

从安全存储读取设备密钥。

**参数**：

- `key` 输出缓冲区。
- `len` 缓冲区长度。

**返回值**：

成功时返回 `0`，失败时返回负值错误码。

### triad_get_hmac

```c
int triad_get_hmac(uint8_t *input, uint16_t inlen,
                   uint8_t *output, uint16_t outlen);
```

使用设备密钥对输入数据做 HMAC 计算，结果写入输出缓冲区。

**参数**：

- `input` 输入数据。
- `inlen` 输入数据长度。
- `output` 输出缓冲区，接收 HMAC 结果。
- `outlen` 输出缓冲区长度。

**返回值**：

成功时返回 `0`，失败时返回负值错误码。

## 微信支付 CA API

对微信安全支付相关数据执行读写操作。实现位于 `frameworks/security/ca/wxcodepay`。

### wxcodepay_tee_data_read

```c
uint32_t wxcodepay_tee_data_read(int item, uint8_t *buff, uint32_t *out_len);
```

读取一条微信支付相关数据项。

**参数**：

- `item` 数据项 ID。
- `buff` 输出缓冲区。
- `out_len` 输入输出参数，返回实际读取长度。

**返回值**：

成功时返回 `TEE_SUCCESS`，失败时返回 TEE 错误码。

### wxcodepay_tee_data_write

```c
uint32_t wxcodepay_tee_data_write(int item, const uint8_t *buf, uint32_t len);
```

写入一条微信支付相关数据项。

**参数**：

- `item` 数据项 ID。
- `buf` 数据缓冲区。
- `len` 数据长度。

**返回值**：

成功时返回 `TEE_SUCCESS`，失败时返回 TEE 错误码。

### wxcodepay_tee_data_delete

```c
uint32_t wxcodepay_tee_data_delete(int item);
```

删除指定微信支付数据项。

**参数**：

- `item` 数据项 ID。

**返回值**：

成功时返回 `TEE_SUCCESS`，失败时返回 TEE 错误码。

### is_wxcodepay_tee_data_exited

```c
bool is_wxcodepay_tee_data_exited(int item);
```

查询指定微信支付数据项是否已存储。

**参数**：

- `item` 数据项 ID。

**返回值**：

存在时返回 `true`，不存在时返回 `false`。

## 支付宝支付 CA API

对支付宝安全支付相关数据执行读写操作。实现位于 `frameworks/security/ca/alipay`。

### alipay_tee_data_read

```c
uint32_t alipay_tee_data_read(const char *item_name, uint8_t *buff,
                              uint32_t *out_len);
```

读取一条支付宝数据项。

**参数**：

- `item_name` 数据项名称字符串。
- `buff` 输出缓冲区。
- `out_len` 输入输出参数，返回实际读取长度。

**返回值**：

成功时返回 `TEE_SUCCESS`，失败时返回 TEE 错误码。

### alipay_tee_data_write

```c
uint32_t alipay_tee_data_write(const char *item_name, const uint8_t *buf,
                               uint32_t len);
```

写入一条支付宝数据项。

**参数**：

- `item_name` 数据项名称字符串。
- `buf` 数据缓冲区。
- `len` 数据长度。

**返回值**：

成功时返回 `TEE_SUCCESS`，失败时返回 TEE 错误码。

### alipay_tee_data_delete

```c
uint32_t alipay_tee_data_delete(const char *item_name);
```

删除指定支付宝数据项。

**参数**：

- `item_name` 数据项名称。

**返回值**：

成功时返回 `TEE_SUCCESS`，失败时返回 TEE 错误码。

### is_alipay_tee_data_exited

```c
bool is_alipay_tee_data_exited(const char *item_name);
```

查询指定支付宝数据项是否已存储。

**参数**：

- `item_name` 数据项名称。

**返回值**：

存在时返回 `true`，不存在时返回 `false`。

## PIN 码 CA API

对个人识别码（Personal Identification Number，PIN）执行存储、验证、修改等操作。实现位于 `frameworks/security/ca/pin`。

### pin_store

```c
uint32_t pin_store(bool is_deletable, uint8_t *buff, uint32_t len);
```

在安全存储中保存一个 PIN。

**参数**：

- `is_deletable` 是否允许被用户侧删除。
- `buff` PIN 数据缓冲区。
- `len` PIN 数据长度。

**返回值**：

成功时返回 `TEE_SUCCESS`，失败时返回 TEE 错误码。

### pin_is_exist

```c
bool pin_is_exist(bool is_deletable);
```

查询指定类型的 PIN 是否已存储。

**参数**：

- `is_deletable` 可删除属性，用于区分不同类型的 PIN。

**返回值**：

存在时返回 `true`，不存在时返回 `false`。

### pin_delete

```c
uint32_t pin_delete(bool is_deletable);
```

删除安全存储中的 PIN。

**参数**：

- `is_deletable` 可删除属性。

**返回值**：

成功时返回 `TEE_SUCCESS`，失败时返回 TEE 错误码。

### pin_verify

```c
uint32_t pin_verify(bool is_deletable, uint8_t *buff, uint32_t len);
```

验证 PIN 是否与安全存储中的记录一致。

**参数**：

- `is_deletable` 可删除属性。
- `buff` 待验证的 PIN 数据。
- `len` PIN 数据长度。

**返回值**：

验证通过返回 `TEE_SUCCESS`，不通过或失败时返回错误码。

### pin_change

```c
uint32_t pin_change(bool is_deletable, uint8_t *old, uint32_t oldlen,
                    uint8_t *new, uint32_t newlen);
```

修改已存储的 PIN，需同时提供旧 PIN 和新 PIN。

**参数**：

- `is_deletable` 可删除属性。
- `old` 旧 PIN 缓冲区。
- `oldlen` 旧 PIN 长度。
- `new` 新 PIN 缓冲区。
- `newlen` 新 PIN 长度。

**返回值**：

成功时返回 `TEE_SUCCESS`（旧 PIN 校验通过且新 PIN 写入成功），失败时返回错误码。

### pin_getsha256

```c
uint32_t pin_getsha256(bool is_deletable, uint8_t *buff, uint32_t len);
```

获取 PIN 对应的 SHA-256 摘要。

**参数**：

- `is_deletable` 可删除属性。
- `buff` 输出缓冲区，接收 32 字节摘要。
- `len` 缓冲区长度（应不小于 32）。

**返回值**：

成功时返回 `TEE_SUCCESS`，失败时返回 TEE 错误码。

## MiTEE Rootkey 管理

Rootkey 是 TEE 安全体系的**信任根密钥**，用于派生其他密钥。该密钥在工厂阶段一次性写入，运行时由 TEE OS 读取使用。

### boardctl_BOARDIOC_UNIQUEKEY

```c
#include <sys/boardctl.h>

boardctl(BOARDIOC_UNIQUEKEY, tmp_key);
```

TEE OS 中的 TEE Server（`miteed`）通过 `boardctl` 系统调用读取 Rootkey。

**参数**：

- `BOARDIOC_UNIQUEKEY` 固定命令字。
- `tmp_key` 输出缓冲区指针，接收 Rootkey 内容。

**返回值**：

成功时返回 `0`，失败时返回负值并设置 `errno`。

**注意**：

- 只有 TEE OS 侧允许调用本接口；REE 侧应用无法访问 Rootkey。

### rootkey_provision

```c
norflash_api_security_register_erase(HAL_FLASH_ID_0, 2048, 32);
norflash_api_security_register_write(HAL_FLASH_ID_0, 2048, rn, 32);
norflash_api_security_register_lock(HAL_FLASH_ID_0, 2048, 32);
```

Rootkey 仅在工厂版本中、TEE OS 首次启动时执行写入。典型流程为"擦除 → 写入 → 锁定"三步：

**参数**（以 `norflash_api_security_register_*` 为例）：

- `HAL_FLASH_ID_0` Flash 设备标识。
- `2048` 安全寄存器起始偏移。
- `32` 字节长度（256 位）。
- `rn` 写入时提供的 Rootkey 数据缓冲区。

**注意**：

- 一旦执行 `_lock`，该区域永久锁定无法再次写入，必须保证写入数据的正确性。
- 生产设备永远不应包含调用上述接口的代码。

## Android Keystore Client API

**本节介绍的 Keystore 是一套独立于 MiTEE 的安全方案**，源码移植自 Android Keystore 服务框架，遵循 Keystore/Keymaster 标准接口。其中 Keymaster 层支持多种实现方式，包括对接 MiTee、纯软件实现以及为安全芯片（SE）定制的实现。

openvela Keystore 向上层以 Keystore C API 的方式，为账号 SDK 等应用场景提供密钥管理与安全存储能力，使用方无需关注底层的硬件差异和具体存储细节。

头文件：`#include <keystore/client.h>`

源码路径：`external/android/system/security/keystore/`

### Keystore 使用约定

- **存储单元**：每条数据通过 `name` 字符串作为唯一标识
- **命名规则**：`name` 长度上限为 `CONFIG_NAME_MAX - 12`；若包含特殊字符（ASCII `0` 至 `~` 范围），每个字符按 2 字节计算
- **返回值约定**：所有接口成功时返回 `KEYSTORE_NO_ERROR`（值为 `1`），失败时返回大于 `1` 的错误码
- **内存管理**：`keyStoreGet` 返回的数据由内部分配，调用方需用 `free()` 释放

### keyStoreInsert

```c
int keyStoreInsert(const char *name, size_t nameLength,
                   const uint8_t *item, size_t itemLength);
```

将一条数据项写入 Keystore，数据在 Keystore 内部加密存储。

**参数**：

- `name` 数据项名称。需唯一，受 `CONFIG_NAME_MAX - 12` 长度限制。
- `nameLength` 名称长度（字节）。
- `item` 要写入的数据缓冲区。
- `itemLength` 数据长度（字节）。

**返回值**：

成功时返回 `KEYSTORE_NO_ERROR`，失败时返回其他 `KEYSTORE_*` 错误码。

### keyStoreGet

```c
int keyStoreGet(const char *name, size_t nameLength,
                uint8_t **item, size_t *itemLength);
```

按名称从 Keystore 读取一条数据项。数据由内部分配，调用方必须通过 `free()` 释放。

**参数**：

- `name` 数据项名称。
- `nameLength` 名称长度。
- `item` 输出参数，返回内部分配的数据缓冲区指针。
- `itemLength` 输出参数，返回数据长度。

**返回值**：

成功时返回 `KEYSTORE_NO_ERROR`，失败时返回其他 `KEYSTORE_*` 错误码。

### keyStoreDel

```c
int keyStoreDel(const char *name, size_t nameLength);
```

按名称删除 Keystore 中的一条数据项。

**参数**：

- `name` 数据项名称。
- `nameLength` 名称长度。

**返回值**：

成功时返回 `KEYSTORE_NO_ERROR`，失败时返回其他 `KEYSTORE_*` 错误码。

### keyStoreExist

```c
int keyStoreExist(const char *name, size_t nameLength);
```

检测 Keystore 中是否存在指定名称的数据项。

**参数**：

- `name` 数据项名称。
- `nameLength` 名称长度。

**返回值**：

存在时返回 `KEYSTORE_NO_ERROR`，不存在或失败时返回其他 `KEYSTORE_*` 错误码。

### keyStoreReset

```c
int keyStoreReset(void);
```

删除当前应用在 Keystore 中的**所有**数据项。

**返回值**：

成功时返回 `KEYSTORE_NO_ERROR`，失败时返回其他 `KEYSTORE_*` 错误码。

**注意**：

- 该操作不可撤销，仅作用于当前应用的命名空间。

### Keystore 错误码

所有 Keystore 接口返回的错误码定义（头文件 `keystore/client.h`）：

| 错误码 | 值 | 含义 |
|--------|----|------|
| `KEYSTORE_NO_ERROR` | 1 | 操作成功 |
| `KEYSTORE_LOCKED` | 2 | Keystore 已锁定 |
| `KEYSTORE_UNINITIALIZED` | 3 | 未初始化 |
| `KEYSTORE_SYSTEM_ERROR` | 4 | 系统错误 |
| `KEYSTORE_PROTOCOL_ERROR` | 5 | 协议错误 |
| `KEYSTORE_PERMISSION_DENIED` | 6 | 权限不足 |
| `KEYSTORE_KEY_NOT_FOUND` | 7 | 指定的数据项不存在 |
| `KEYSTORE_VALUE_CORRUPTED` | 8 | 数据损坏 |
| `KEYSTORE_UNDEFINED_ACTION` | 9 | 未定义的操作 |
| `KEYSTORE_WRONG_PASSWORD_0` ~ `KEYSTORE_WRONG_PASSWORD_3` | 10-13 | 密码错误（最多 4 次重试） |
| `KEYSTORE_SIGNATURE_INVALID` | 14 | 签名无效 |
| `KEYSTORE_OP_AUTH_NEEDED` | 15 | 本次操作需要先通过身份认证 |
| `KEYSTORE_KEY_ALREADY_EXISTS` | 16 | 数据项已存在 |
| `KEYSTORE_KEY_PERMANENTLY_INVALIDATED` | 17 | 数据项永久失效 |
| `KEYSTORE_ABORT_CALLED` | 18 | 操作被中止 |
| `KEYSTORE_PRUNED` | 19 | 数据被 pruned |
| `KEYSTORE_BINDER_DIED` | 20 | Binder 连接已断开 |

## GP TEE Client API（REE 侧）

以下接口遵循 GlobalPlatform TEE Client API 规范，由 CA 在 REE 侧调用，用于与 TEE 建立上下文、打开会话、执行命令。

### TEEC_InitializeContext

```c
TEEC_Result TEEC_InitializeContext(const char *name, TEEC_Context *context);
```

初始化一个 TEE 上下文，建立 CA 与指定 TEE 之间的连接。

**参数**：

- `name` 零结尾字符串，标识要连接的 TEE。当前实现仅支持 `NULL`，表示连接默认 TEE。
- `context` 待初始化的上下文结构体指针。

**返回值**：

成功时返回 `TEEC_SUCCESS`，失败时返回其他 `TEEC_Result` 错误码。

### TEEC_FinalizeContext

```c
void TEEC_FinalizeContext(TEEC_Context *context);
```

销毁已初始化的 TEE 上下文，关闭 CA 与 TEE 之间的连接。

**参数**：

- `context` 要销毁的上下文。

**注意**：

- 调用前必须确保所有关联的会话已关闭、所有共享内存已释放。

### TEEC_OpenSession

```c
TEEC_Result TEEC_OpenSession(TEEC_Context *context,
                             TEEC_Session *session,
                             const TEEC_UUID *destination,
                             uint32_t connectionMethod,
                             const void *connectionData,
                             TEEC_Operation *operation,
                             uint32_t *returnOrigin);
```

在 CA 与指定 TA 之间打开一个新会话。

**参数**：

- `context` 已初始化的 TEE 上下文。
- `session` 待初始化的会话结构体指针。
- `destination` 目标 TA 的 UUID。
- `connectionMethod` 连接方式。
- `connectionData` 连接相关数据（当前未使用，应传 `NULL`）。
- `operation` 操作参数结构体；若不需要传参，可传 `NULL`。
- `returnOrigin` 输出参数，错误发生时返回错误来源。

**返回值**：

成功时返回 `TEEC_SUCCESS`，失败时返回其他 `TEEC_Result` 错误码。

### TEEC_CloseSession

```c
void TEEC_CloseSession(TEEC_Session *session);
```

关闭已打开的 TA 会话。

**参数**：

- `session` 要关闭的会话。

### TEEC_InvokeCommand

```c
TEEC_Result TEEC_InvokeCommand(TEEC_Session *session,
                               uint32_t commandID,
                               TEEC_Operation *operation,
                               uint32_t *returnOrigin);
```

在指定会话中调用 TA 命令。

**参数**：

- `session` 已打开的会话句柄。
- `commandID` TA 内部的命令 ID。
- `operation` 操作参数结构体；若不需要传参，可传 `NULL`。
- `returnOrigin` 输出参数，错误发生时返回错误来源。

**返回值**：

成功时返回 `TEEC_SUCCESS`，失败时返回其他 `TEEC_Result` 错误码。

### TEEC_AllocateSharedMemory

```c
TEEC_Result TEEC_AllocateSharedMemory(TEEC_Context *context,
                                      TEEC_SharedMemory *sharedMem);
```

在指定 TEE 上下文范围内分配一块共享内存。

**参数**：

- `context` 已初始化的 TEE 上下文。
- `sharedMem` 待分配的共享内存结构体指针。

**返回值**：

成功时返回 `TEEC_SUCCESS`；内存不足时返回 `TEEC_ERROR_OUT_OF_MEMORY`；其他失败返回对应 `TEEC_Result` 错误码。

### TEEC_RegisterSharedMemory

```c
TEEC_Result TEEC_RegisterSharedMemory(TEEC_Context *context,
                                      TEEC_SharedMemory *sharedMem);
```

将一块**调用方已分配**的内存注册为共享内存。与 `TEEC_AllocateSharedMemory`（由框架分配）不同，本接口允许 CA 复用已有内存缓冲区作为 TEE 通信数据区。

**参数**：

- `context` 已初始化的 TEE 上下文。
- `sharedMem` 共享内存结构体指针，调用方应预先填写 `buffer`、`size` 和 `flags` 字段。

**返回值**：

成功时返回 `TEEC_SUCCESS`，失败时返回对应 `TEEC_Result` 错误码。

### TEEC_ReleaseSharedMemory

```c
void TEEC_ReleaseSharedMemory(TEEC_SharedMemory *sharedMemory);
```

释放或注销先前分配的共享内存块。对 `TEEC_AllocateSharedMemory` 分配的内存会释放，对 `TEEC_RegisterSharedMemory` 注册的内存只做注销（不释放调用方的缓冲区）。

**参数**：

- `sharedMemory` 待释放的共享内存结构体指针。

### TEEC_RequestCancellation

```c
void TEEC_RequestCancellation(TEEC_Operation *operation);
```

请求取消一个正在执行的 `TEEC_OpenSession` 或 `TEEC_InvokeCommand` 操作。调用本接口后，对应操作可能被 TEE 异步中止。

**参数**：

- `operation` 目标操作的 `TEEC_Operation` 结构体指针。该结构必须是某个正在执行中的 `OpenSession` / `InvokeCommand` 使用的同一份对象。

**注意**：

- 本接口是"请求"而非"强制"，能否真正中止由 TEE 和目标 TA 决定。
- TA 需要在 GP Internal API 中调用 `TEE_GetCancellationFlag` 配合才能响应取消请求。

## GP TEE Internal API（TEE 侧）

GP TEE Internal Core API 是 GlobalPlatform 定义的标准 TA 开发接口，**函数签名、参数语义和返回值语义以 GP 官方规范为准**。openvela 的 MiTEE 在兼容这些接口的同时，由于当前实现进度原因，部分接口仅处于"实现不完整"状态。

> **权威参考**：
> - [GlobalPlatform TEE Internal Core API Specification v1.3.1](https://globalplatform.org/specs-library/tee-internal-core-api-specification/)
> - `optee_os` 源码中的 `<tee_internal_api.h>`

本节以**状态速查表**的形式列出 openvela 对每个 GP Internal API 的支持情况，便于 TA 开发者判断哪些 API 可以直接使用。完整签名、参数、返回值请以上述 GP 官方规范为准。

**状态列说明**：

- **支持** — openvela 已完整实现，行为与 GP 规范一致
- **实现不完整** — 函数符号存在，但部分行为尚未实现或未经充分验证，不建议生产环境使用

### TA 生命周期入口

| 函数 | 状态 | 描述 |
| --- | --- | --- |
| `TA_CreateEntryPoint` | 支持 | TA 创建入口 |
| `TA_DestroyEntryPoint` | 支持 | TA 销毁入口 |
| `TA_OpenSessionEntryPoint` | 支持 | 会话打开入口 |
| `TA_CloseSessionEntryPoint` | 支持 | 会话关闭入口 |
| `TA_InvokeCommandEntryPoint` | 支持 | 命令调用入口 |

### TA 间通信

| 函数 | 状态 | 描述 |
| --- | --- | --- |
| `TEE_OpenTASession` | 实现不完整 | 打开 TA 间会话 |
| `TEE_CloseTASession` | 实现不完整 | 关闭 TA 间会话 |
| `TEE_InvokeTACommand` | 实现不完整 | 调用其他 TA 命令 |

### 内存访问检查

| 函数 | 状态 | 描述 |
| --- | --- | --- |
| `TEE_CheckMemoryAccessRights` | 实现不完整 | 检查内存访问权限 |

### 内存管理

| 函数 | 状态 | 描述 |
| --- | --- | --- |
| `TEE_Malloc` | 支持 | 分配内存 |
| `TEE_Realloc` | 支持 | 重新分配内存 |
| `TEE_Free` | 支持 | 释放内存 |
| `TEE_MemMove` | 支持 | 内存移动 |
| `TEE_MemCompare` | 支持 | 内存比较 |
| `TEE_MemFill` | 支持 | 内存填充 |

### 通用对象操作

| 函数 | 状态 | 描述 |
| --- | --- | --- |
| `TEE_GetObjectInfo1` | 支持 | 获取对象信息 |
| `TEE_CloseObject` | 支持 | 关闭对象 |

### 瞬态对象操作

| 函数 | 状态 | 描述 |
| --- | --- | --- |
| `TEE_AllocateTransientObject` | 支持 | 分配瞬态对象 |
| `TEE_FreeTransientObject` | 支持 | 释放瞬态对象 |
| `TEE_ResetTransientObject` | 支持 | 重置瞬态对象 |
| `TEE_PopulateTransientObject` | 支持 | 填充瞬态对象属性 |
| `TEE_InitRefAttribute` | 支持 | 初始化引用属性 |
| `TEE_InitValueAttribute` | 支持 | 初始化值属性 |
| `TEE_CopyObjectAttributes1` | 支持 | 复制对象属性 |
| `TEE_GenerateKey` | 实现不完整 | 生成密钥 |

### 持久化对象操作

| 函数 | 状态 | 描述 |
| --- | --- | --- |
| `TEE_OpenPersistentObject` | 实现不完整 | 打开持久化对象 |
| `TEE_CreatePersistentObject` | 实现不完整 | 创建持久化对象 |
| `TEE_CloseAndDeletePersistentObject` | 实现不完整 | 关闭并删除持久化对象 |
| `TEE_RenamePersistentObject` | 实现不完整 | 重命名持久化对象 |

### 持久化对象数据流操作

| 函数 | 状态 | 描述 |
| --- | --- | --- |
| `TEE_ReadObjectData` | 实现不完整 | 读取对象数据 |
| `TEE_WriteObjectData` | 实现不完整 | 写入对象数据 |
| `TEE_TruncateObjectData` | 实现不完整 | 截断对象数据 |
| `TEE_SeekObjectData` | 实现不完整 | 定位对象数据偏移 |

### 密码学操作管理

| 函数 | 状态 | 描述 |
| --- | --- | --- |
| `TEE_AllocateOperation` | 支持 | 分配密码学操作 |
| `TEE_FreeOperation` | 支持 | 释放密码学操作 |
| `TEE_GetOperationInfo` | 支持 | 获取操作信息 |
| `TEE_GetOperationInfoMultiple` | 支持 | 获取多密钥操作信息 |
| `TEE_ResetOperation` | 支持 | 重置操作 |
| `TEE_SetOperationKey` | 支持 | 设置操作密钥 |
| `TEE_SetOperationKey2` | 支持 | 设置双密钥操作 |
| `TEE_CopyOperation` | 支持 | 复制操作 |

### 消息摘要（Message Digest）

| 函数 | 状态 | 描述 |
| --- | --- | --- |
| `TEE_DigestUpdate` | 支持 | 更新摘要数据 |
| `TEE_DigestDoFinal` | 支持 | 完成摘要计算 |

### 对称加密（Symmetric Cipher）

| 函数 | 状态 | 描述 |
| --- | --- | --- |
| `TEE_CipherInit` | 支持 | 初始化对称加密操作 |
| `TEE_CipherUpdate` | 支持 | 更新加密数据 |
| `TEE_CipherDoFinal` | 支持 | 完成加密操作 |

### 消息认证码（MAC）

| 函数 | 状态 | 描述 |
| --- | --- | --- |
| `TEE_MACInit` | 支持 | 初始化 MAC 操作 |
| `TEE_MACUpdate` | 支持 | 更新 MAC 数据 |
| `TEE_MACComputeFinal` | 支持 | 计算最终 MAC 值 |
| `TEE_MACCompareFinal` | 支持 | 比较最终 MAC 值 |

### 认证加密（Authenticated Encryption，AE）

| 函数 | 状态 | 描述 |
| --- | --- | --- |
| `TEE_AEInit` | 实现不完整 | 初始化 AE 操作 |
| `TEE_AEUpdateAAD` | 实现不完整 | 更新附加认证数据 |
| `TEE_AEUpdate` | 实现不完整 | 更新 AE 数据 |
| `TEE_AEEncryptFinal` | 实现不完整 | 完成 AE 加密 |
| `TEE_AEDecryptFinal` | 实现不完整 | 完成 AE 解密 |

### 非对称加密（Asymmetric Cryptography）

| 函数 | 状态 | 描述 |
| --- | --- | --- |
| `TEE_AsymmetricEncrypt` | 实现不完整 | 非对称加密 |
| `TEE_AsymmetricDecrypt` | 实现不完整 | 非对称解密 |
| `TEE_AsymmetricSignDigest` | 实现不完整 | 非对称签名 |
| `TEE_AsymmetricVerifyDigest` | 实现不完整 | 非对称验签 |

### 密钥派生（Key Derivation）

| 函数 | 状态 | 描述 |
| --- | --- | --- |
| `TEE_DeriveKey` | 实现不完整 | 派生密钥 |

### 随机数生成

| 函数 | 状态 | 描述 |
| --- | --- | --- |
| `TEE_GenerateRandom` | 实现不完整 | 生成随机数 |

### 时间 API

| 函数 | 状态 | 描述 |
| --- | --- | --- |
| `TEE_GetSystemTime` | 实现不完整 | 获取系统时间 |
| `TEE_GetTAPersistentTime` | 实现不完整 | 获取 TA 持久化时间 |
| `TEE_SetTAPersistentTime` | 实现不完整 | 设置 TA 持久化时间 |
| `TEE_GetREETime` | 实现不完整 | 获取 REE 时间 |
