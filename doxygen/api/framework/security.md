# 安全框架 API（Security Framework API）

openvela 安全框架基于 MiTEE（可信执行环境）提供安全存储、密钥管理和安全支付等能力，遵循 GlobalPlatform（GP）TEE 标准。

本文档涵盖以下内容：

- MiTEE CA 应用级 API 接口
- MiTEE Rootkey API 接口
- mitee_iot 框架层 API 接口（GP TEE Client API 与 GP TEE Internal API）

## 一、MiTEE CA 应用级 API 接口

CA 应用级接口封装了常见的安全业务操作，开发者可直接调用这些接口完成安全存储读写、设备身份验证、安全支付等功能。

### 1、通用安全存储 SST CA API

对安全存储（Secure Storage，SST）分区执行读写操作。

实现位于：`frameworks/security/ca/comsst`

```c
uint32_t comsst_data_read(uint8_t *scope, uint8_t *name, bool is_deletable,
    uint8_t *buff, uint32_t *out_len);
uint32_t comsst_data_write(uint8_t *scope, uint8_t *name, bool is_deletable,
    uint8_t *buff, uint32_t len);
uint32_t comsst_data_delete(uint8_t *scope, uint8_t *name, bool is_deletable);
uint32_t is_comsst_data_exited(uint8_t *scope, uint8_t *name,
    bool is_deletable);
uint32_t comsst_data_verify(uint8_t *scope, uint8_t *name, bool is_deletable,
    uint8_t *buff, uint32_t len);
```

### 2、三元组 CA API

对设备三元组中的设备标识（DID）和密钥（Key）执行读写操作。

实现位于：`frameworks/security/ca/triad`

```c
int triad_store_did(uint8_t* did, uint16_t len);
int triad_load_did(uint8_t* did, uint16_t len);
int triad_store_key(uint8_t* key, uint16_t len);
int triad_load_key(uint8_t* key, uint16_t len);
int triad_get_hmac(uint8_t* input, uint16_t inlen,
    uint8_t* output, uint16_t outlen);
```

### 3、微信支付 CA API

对微信安全支付相关数据执行读写操作。

实现位于：`frameworks/security/ca/wxcodepay`

```c
uint32_t wxcodepay_tee_data_read(int item, uint8_t* buff, uint32_t* out_len);
uint32_t wxcodepay_tee_data_write(int item, const uint8_t* buf, uint32_t len);
uint32_t wxcodepay_tee_data_delete(int item);
bool is_wxcodepay_tee_data_exited(int item);
```

### 4、支付宝支付 CA API

对支付宝安全支付相关数据执行读写操作。

实现位于：`frameworks/security/ca/alipay`

```c
uint32_t alipay_tee_data_read(const char* item_name, uint8_t* buff,
    uint32_t* out_len);
uint32_t alipay_tee_data_write(const char* item_name, const uint8_t* buf,
    uint32_t len);
uint32_t alipay_tee_data_delete(const char* item_name);
bool is_alipay_tee_data_exited(const char* item_name);
```

### 5、PIN 码 CA API

对个人识别码（Personal Identification Number，PIN）执行存储、验证、修改等操作。

实现位于：`frameworks/security/ca/pin`

```c
uint32_t pin_store(bool is_deletable, uint8_t *buff, uint32_t len);
bool pin_is_exist(bool is_deletable);
uint32_t pin_delete(bool is_deletable);
uint32_t pin_verify(bool is_deletable, uint8_t *buff, uint32_t len);
uint32_t pin_change(bool is_deletable, uint8_t *old, uint32_t oldlen,
    uint8_t *new, uint32_t newlen);
uint32_t pin_getsha256(bool is_deletable, uint8_t *buff, uint32_t len);
```

## 二、MiTEE Rootkey API 接口

Rootkey 是 TEE 安全体系的信任根密钥，用于派生其他密钥。该密钥在工厂阶段一次性写入，运行时由 TEE OS 读取使用。

### 1、读取 Rootkey

TEE OS 中的 TEE Server（miteed）通过以下接口获取 Rootkey：

```c
#include <sys/boardctl.h>
boardctl(BOARDIOC_UNIQUEKEY, tmp_key);
```

### 2、写入 Rootkey

Rootkey 仅在工厂版本中、TEE OS 首次启动时执行 `rootkey_provision` 写入。

<!-- ⚠️ 安全合规：已移除内部 vendor 路径（vendor/xiaomi/miwear/factest/rootkey_provision），如需引用请使用脱敏路径。 -->

```c
norflash_api_security_register_erase(HAL_FLASH_ID_0, 2048, 32)
norflash_api_security_register_write(HAL_FLASH_ID_0, 2048, rn, 32)
norflash_api_security_register_lock(HAL_FLASH_ID_0, 2048, 32)
```

## 三、mitee_iot 框架层 API 接口

mitee_iot 框架层包含两部分：

- **TEE Client（libteec）**：运行在普通执行环境（Rich Execution Environment，REE）侧，实现 GP TEE Client API，供 CA 调用以发起 TEE 请求。
- **TEE Server（miteed）**：运行在 TEE 侧，接收并处理 CA 发起的请求，实现 GP TEE Internal API。

> TEE Client 与 TEE Server 之间通过 rpmsg socket 进行数据交换。

### 1、GP TEE Client API

以下接口遵循 GlobalPlatform TEE Client API 规范，供 CA 在 REE 侧调用。

#### TEEC_InitializeContext

初始化一个 TEE 上下文，建立 CA 与指定 TEE 之间的连接。

```c
/**
 * TEEC_InitializeContext() - Initializes a context holding connection
 * information on the specific TEE, designated by the name string.
 *
 * @param name    A zero-terminated string identifying the TEE to connect to.
 *                If name is set to NULL, the default TEE is connected to. NULL
 *                is the only supported value in this version of the API
 *                implementation.
 *
 * @param context The context structure which is to be initialized.
 *
 * @return TEEC_SUCCESS  The initialization was successful.
 * @return TEEC_Result   Something failed.
 */
TEEC_Result TEEC_InitializeContext(const char *name, TEEC_Context *context);
```

#### TEEC_FinalizeContext

销毁已初始化的 TEE 上下文，关闭 CA 与 TEE 之间的连接。调用前需确保所有关联的会话已关闭、所有共享内存已释放。

```c
/**
 * TEEC_FinalizeContext() - Destroys a context holding connection information
 * on the specific TEE.
 *
 * This function destroys an initialized TEE context, closing the connection
 * between the client application and the TEE. This function must only be
 * called when all sessions related to this TEE context have been closed and
 * all shared memory blocks have been released.
 *
 * @param context The context to be destroyed.
 */
void TEEC_FinalizeContext(TEEC_Context *context);
```

#### TEEC_OpenSession

在 CA 与指定 TA 之间打开一个新会话。

```c
/**
 * TEEC_OpenSession() - Opens a new session with the specified trusted
 * application.
 *
 * @param context          The initialized TEE context structure in which
 *                         scope to open the session.
 * @param session          The session to initialize.
 * @param destination      A structure identifying the trusted application
 *                         with which to open a session.
 * @param connectionMethod The connection method to use.
 * @param connectionData   Any data necessary to connect with the chosen
 *                         connection method. Not supported, should be set to
 *                         NULL.
 * @param operation        An operation structure to use in the session. May
 *                         be set to NULL to signify no operation structure
 *                         needed.
 * @param returnOrigin     A parameter which will hold the error origin if
 *                         this function returns any value other than
 *                         TEEC_SUCCESS.
 *
 * @return TEEC_SUCCESS  OpenSession successfully opened a new session.
 * @return TEEC_Result   Something failed.
 */
TEEC_Result TEEC_OpenSession(TEEC_Context *context,
    TEEC_Session *session,
    const TEEC_UUID *destination,
    uint32_t connectionMethod,
    const void *connectionData,
    TEEC_Operation *operation,
    uint32_t *returnOrigin);
```

#### TEEC_CloseSession

关闭已打开的 TA 会话。

```c
/**
 * TEEC_CloseSession() - Closes the session which has been opened with the
 * specific trusted application.
 *
 * @param session The opened session to close.
 */
void TEEC_CloseSession(TEEC_Session *session);
```

#### TEEC_InvokeCommand

在指定会话中调用 TA 命令。

```c
/**
 * TEEC_InvokeCommand() - Executes a command in the specified trusted
 * application.
 *
 * @param session      A handle to an open connection to the trusted
 *                     application.
 * @param commandID    Identifier of the command in the trusted application
 *                     to invoke.
 * @param operation    An operation structure to use in the invoke command.
 *                     May be set to NULL to signify no operation structure
 *                     needed.
 * @param returnOrigin A parameter which will hold the error origin if this
 *                     function returns any value other than TEEC_SUCCESS.
 *
 * @return TEEC_SUCCESS  Command invoked successfully.
 * @return TEEC_Result   Something failed.
 */
TEEC_Result TEEC_InvokeCommand(TEEC_Session *session,
    uint32_t commandID,
    TEEC_Operation *operation,
    uint32_t *returnOrigin);
```

#### TEEC_AllocateSharedMemory

在指定 TEE 上下文范围内分配一块共享内存。

```c
/**
 * TEEC_AllocateSharedMemory() - Allocate shared memory for TEE.
 *
 * @param context   The initialized TEE context structure in which scope to
 *                  open the session.
 * @param sharedMem Pointer to the allocated shared memory.
 *
 * @return TEEC_SUCCESS            The allocation was successful.
 * @return TEEC_ERROR_OUT_OF_MEMORY Memory exhaustion.
 * @return TEEC_Result             Something failed.
 */
TEEC_Result TEEC_AllocateSharedMemory(TEEC_Context *context,
    TEEC_SharedMemory *sharedMem);
```

#### TEEC_ReleaseSharedMemory

释放或注销先前分配的共享内存块。

```c
/**
 * TEEC_ReleaseSharedMemory() - Free or deregister the shared memory.
 *
 * @param sharedMemory Pointer to the shared memory to be freed.
 */
void TEEC_ReleaseSharedMemory(TEEC_SharedMemory *sharedMemory);
```

### 2、GP TEE Internal API

以下为 TEE Server（miteed）上支持的 GP TEE Internal API 列表及实现状态。

#### TA 生命周期入口

| 函数                       | 状态 | 描述         |
| -------------------------- | ---- | ------------ |
| TA_CreateEntryPoint        | 支持 | TA 创建入口  |
| TA_DestroyEntryPoint       | 支持 | TA 销毁入口  |
| TA_OpenSessionEntryPoint   | 支持 | 会话打开入口 |
| TA_CloseSessionEntryPoint  | 支持 | 会话关闭入口 |
| TA_InvokeCommandEntryPoint | 支持 | 命令调用入口 |

#### TA 间通信

| 函数                | 状态       | 描述             |
| ------------------- | ---------- | ---------------- |
| TEE_OpenTASession   | 实现不完整 | 打开 TA 间会话   |
| TEE_CloseTASession  | 实现不完整 | 关闭 TA 间会话   |
| TEE_InvokeTACommand | 实现不完整 | 调用其他 TA 命令 |

#### 内存访问检查

| 函数                        | 状态       | 描述             |
| --------------------------- | ---------- | ---------------- |
| TEE_CheckMemoryAccessRights | 实现不完整 | 检查内存访问权限 |

#### 内存管理

| 函数           | 状态 | 描述         |
| -------------- | ---- | ------------ |
| TEE_Malloc     | 支持 | 分配内存     |
| TEE_Realloc    | 支持 | 重新分配内存 |
| TEE_Free       | 支持 | 释放内存     |
| TEE_MemMove    | 支持 | 内存移动     |
| TEE_MemCompare | 支持 | 内存比较     |
| TEE_MemFill    | 支持 | 内存填充     |

#### 通用对象操作

| 函数               | 状态 | 描述         |
| ------------------ | ---- | ------------ |
| TEE_GetObjectInfo1 | 支持 | 获取对象信息 |
| TEE_CloseObject    | 支持 | 关闭对象     |

#### 瞬态对象操作

| 函数                        | 状态       | 描述             |
| --------------------------- | ---------- | ---------------- |
| TEE_AllocateTransientObject | 支持       | 分配瞬态对象     |
| TEE_FreeTransientObject     | 支持       | 释放瞬态对象     |
| TEE_ResetTransientObject    | 支持       | 重置瞬态对象     |
| TEE_PopulateTransientObject | 支持       | 填充瞬态对象属性 |
| TEE_InitRefAttribute        | 支持       | 初始化引用属性   |
| TEE_InitValueAttribute      | 支持       | 初始化值属性     |
| TEE_CopyObjectAttributes1   | 支持       | 复制对象属性     |
| TEE_GenerateKey             | 实现不完整 | 生成密钥         |

#### 持久化对象操作

| 函数                               | 状态       | 描述                 |
| ---------------------------------- | ---------- | -------------------- |
| TEE_OpenPersistentObject           | 实现不完整 | 打开持久化对象       |
| TEE_CreatePersistentObject         | 实现不完整 | 创建持久化对象       |
| TEE_CloseAndDeletePersistentObject | 实现不完整 | 关闭并删除持久化对象 |
| TEE_RenamePersistentObject         | 实现不完整 | 重命名持久化对象     |

#### 持久化对象数据流操作

| 函数                   | 状态       | 描述             |
| ---------------------- | ---------- | ---------------- |
| TEE_ReadObjectData     | 实现不完整 | 读取对象数据     |
| TEE_WriteObjectData    | 实现不完整 | 写入对象数据     |
| TEE_TruncateObjectData | 实现不完整 | 截断对象数据     |
| TEE_SeekObjectData     | 实现不完整 | 定位对象数据偏移 |

#### 密码学操作管理

| 函数                         | 状态 | 描述               |
| ---------------------------- | ---- | ------------------ |
| TEE_AllocateOperation        | 支持 | 分配密码学操作     |
| TEE_FreeOperation            | 支持 | 释放密码学操作     |
| TEE_GetOperationInfo         | 支持 | 获取操作信息       |
| TEE_GetOperationInfoMultiple | 支持 | 获取多密钥操作信息 |
| TEE_ResetOperation           | 支持 | 重置操作           |
| TEE_SetOperationKey          | 支持 | 设置操作密钥       |
| TEE_SetOperationKey2         | 支持 | 设置双密钥操作     |
| TEE_CopyOperation            | 支持 | 复制操作           |

#### 消息摘要（Message Digest）

| 函数              | 状态 | 描述         |
| ----------------- | ---- | ------------ |
| TEE_DigestUpdate  | 支持 | 更新摘要数据 |
| TEE_DigestDoFinal | 支持 | 完成摘要计算 |

#### 对称加密（Symmetric Cipher）

| 函数              | 状态 | 描述               |
| ----------------- | ---- | ------------------ |
| TEE_CipherInit    | 支持 | 初始化对称加密操作 |
| TEE_CipherUpdate  | 支持 | 更新加密数据       |
| TEE_CipherDoFinal | 支持 | 完成加密操作       |

#### 消息认证码（MAC）

| 函数                | 状态 | 描述            |
| ------------------- | ---- | --------------- |
| TEE_MACInit         | 支持 | 初始化 MAC 操作 |
| TEE_MACUpdate       | 支持 | 更新 MAC 数据   |
| TEE_MACComputeFinal | 支持 | 计算最终 MAC 值 |
| TEE_MACCompareFinal | 支持 | 比较最终 MAC 值 |

#### 认证加密（Authenticated Encryption，AE）

| 函数               | 状态       | 描述             |
| ------------------ | ---------- | ---------------- |
| TEE_AEInit         | 实现不完整 | 初始化 AE 操作   |
| TEE_AEUpdateAAD    | 实现不完整 | 更新附加认证数据 |
| TEE_AEUpdate       | 实现不完整 | 更新 AE 数据     |
| TEE_AEEncryptFinal | 实现不完整 | 完成 AE 加密     |
| TEE_AEDecryptFinal | 实现不完整 | 完成 AE 解密     |

#### 非对称加密（Asymmetric Cryptography）

| 函数                       | 状态       | 描述       |
| -------------------------- | ---------- | ---------- |
| TEE_AsymmetricEncrypt      | 实现不完整 | 非对称加密 |
| TEE_AsymmetricDecrypt      | 实现不完整 | 非对称解密 |
| TEE_AsymmetricSignDigest   | 实现不完整 | 非对称签名 |
| TEE_AsymmetricVerifyDigest | 实现不完整 | 非对称验签 |

#### 密钥派生（Key Derivation）

| 函数          | 状态       | 描述     |
| ------------- | ---------- | -------- |
| TEE_DeriveKey | 实现不完整 | 派生密钥 |

#### 随机数生成

| 函数               | 状态       | 描述       |
| ------------------ | ---------- | ---------- |
| TEE_GenerateRandom | 实现不完整 | 生成随机数 |

#### 时间 API

| 函数                    | 状态       | 描述               |
| ----------------------- | ---------- | ------------------ |
| TEE_GetSystemTime       | 实现不完整 | 获取系统时间       |
| TEE_GetTAPersistentTime | 实现不完整 | 获取 TA 持久化时间 |
| TEE_SetTAPersistentTime | 实现不完整 | 设置 TA 持久化时间 |
| TEE_GetREETime          | 实现不完整 | 获取 REE 时间      |
