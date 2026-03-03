# openvela Security Framework API

openvela 安全框架基于 MiTEE（可信执行环境）提供安全存储、密钥管理和安全支付等能力，遵循 GlobalPlatform（GP）TEE 标准。

## 一、MiTEE CA 应用级 API 接口

### 1、通用安全存储 SST CA API

对安全存储 /sst 分区的读写操作：

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

对设备三元组中的 did 和 key 读写操作：

```c
int triad_store_did(uint8_t* did, uint16_t len);
int triad_load_did(uint8_t* did, uint16_t len);
int triad_store_key(uint8_t* key, uint16_t len);
int triad_load_key(uint8_t* key, uint16_t len);
int triad_get_hmac(uint8_t* input, uint16_t inlen,
    uint8_t* output, uint16_t outlen);
```

### 3、PIN 码 CA API

对 PIN 码的读写操作：

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

### 1、读取 rootkey

TEE OS 中的 tee server miteed 通过如下接口获取 rootkey：

```c
#include <sys/boardctl.h>
boardctl(BOARDIOC_UNIQUEKEY, tmp_key);
```

## 三、TEE Client API

TEE Client 实现部分 GP TEE Client API，TEE Client 与 TEE Server 之间采用 rpmsg socket 进行数据交换。

### 1、TEEC_InitializeContext

初始化一个新的 TEE Context，建立 Client Application 与 TEE 之间的连接。

```c
TEEC_Result TEEC_InitializeContext(const char *name, TEEC_Context *context);
```

### 2、TEEC_FinalizeContext

销毁已初始化的 TEE Context，关闭 Client Application 与 TEE 之间的连接。

```c
void TEEC_FinalizeContext(TEEC_Context *context);
```

### 3、TEEC_OpenSession

在 Client Application 与指定 Trusted Application 之间打开一个新的 Session。

```c
TEEC_Result TEEC_OpenSession(TEEC_Context *context,
    TEEC_Session *session,
    const TEEC_UUID *destination,
    uint32_t connectionMethod,
    const void *connectionData,
    TEEC_Operation *operation,
    uint32_t *returnOrigin);
```

### 4、TEEC_CloseSession

关闭与 Trusted Application 之间已打开的 Session。

```c
void TEEC_CloseSession(TEEC_Session *session);
```

### 5、TEEC_InvokeCommand

在指定 Session 中调用一个命令。

```c
TEEC_Result TEEC_InvokeCommand(TEEC_Session *session,
    uint32_t commandID,
    TEEC_Operation *operation,
    uint32_t *returnOrigin);
```

### 6、TEEC_AllocateSharedMemory

在指定 TEE Context 范围内分配一块共享内存。

```c
TEEC_Result TEEC_AllocateSharedMemory(TEEC_Context *context,
    TEEC_SharedMemory *sharedMem);
```

### 7、TEEC_ReleaseSharedMemory

释放或注销之前初始化的共享内存块。

```c
void TEEC_ReleaseSharedMemory(TEEC_SharedMemory *sharedMemory);
```

## 四、GP Internal API 支持状态

TEE Server 上支持的 GP Internal API 列表：

| 函数                               | 状态       |
| :--------------------------------- | :--------- |
| TA_CreateEntryPoint                | 支持       |
| TA_DestroyEntryPoint               | 支持       |
| TA_OpenSessionEntryPoint           | 支持       |
| TA_CloseSessionEntryPoint          | 支持       |
| TA_InvokeCommandEntryPoint         | 支持       |
| TEE_OpenTASession                  | 实现不完整 |
| TEE_CloseTASession                 | 实现不完整 |
| TEE_InvokeTACommand                | 实现不完整 |
| TEE_CheckMemoryAccessRights        | 实现不完整 |
| TEE_Malloc                         | 支持       |
| TEE_Realloc                        | 支持       |
| TEE_Free                           | 支持       |
| TEE_MemMove                        | 支持       |
| TEE_MemCompare                     | 支持       |
| TEE_MemFill                        | 支持       |
| TEE_GetObjectInfo1                 | 支持       |
| TEE_CloseObject                    | 支持       |
| TEE_AllocateTransientObject        | 支持       |
| TEE_FreeTransientObject            | 支持       |
| TEE_ResetTransientObject           | 支持       |
| TEE_PopulateTransientObject        | 支持       |
| TEE_InitRefAttribute               | 支持       |
| TEE_InitValueAttribute             | 支持       |
| TEE_CopyObjectAttributes1          | 支持       |
| TEE_GenerateKey                    | 实现不完整 |
| TEE_OpenPersistentObject           | 实现不完整 |
| TEE_CreatePersistentObject         | 实现不完整 |
| TEE_CloseAndDeletePersistentObject | 实现不完整 |
| TEE_RenamePersistentObject         | 实现不完整 |
| TEE_ReadObjectData                 | 实现不完整 |
| TEE_WriteObjectData                | 实现不完整 |
| TEE_TruncateObjectData             | 实现不完整 |
| TEE_SeekObjectData                 | 实现不完整 |
| TEE_AllocateOperation              | 支持       |
| TEE_FreeOperation                  | 支持       |
| TEE_GetOperationInfo               | 支持       |
| TEE_GetOperationInfoMultiple       | 支持       |
| TEE_ResetOperation                 | 支持       |
| TEE_SetOperationKey                | 支持       |
| TEE_SetOperationKey2               | 支持       |
| TEE_CopyOperation                  | 支持       |
| TEE_DigestUpdate                   | 支持       |
| TEE_DigestDoFinal                  | 支持       |
| TEE_CipherInit                     | 支持       |
| TEE_CipherUpdate                   | 支持       |
| TEE_CipherDoFinal                  | 支持       |
| TEE_MACInit                        | 支持       |
| TEE_MACUpdate                      | 支持       |
| TEE_MACComputeFinal                | 支持       |
| TEE_MACCompareFinal                | 支持       |
| TEE_AEInit                         | 实现不完整 |
| TEE_AEUpdateAAD                    | 实现不完整 |
| TEE_AEUpdate                       | 实现不完整 |
| TEE_AEEncrypt                      | 实现不完整 |
| TEE_AEDecrypt                      | 实现不完整 |
| TEE_AsymmetricEncrypt              | 实现不完整 |
| TEE_AsymmetricDecrypt              | 实现不完整 |
| TEE_AsymmetricSignDigest           | 实现不完整 |
| TEE_AsymmetricVerifyDigest         | 实现不完整 |
| TEE_DeriveKey                      | 实现不完整 |
| TEE_GenerateRandom                 | 实现不完整 |
| TEE_GetSystemTime                  | 实现不完整 |
| TEE_GetTAPersistentTime            | 实现不完整 |
| TEE_SetTAPersistentTime            | 实现不完整 |
| TEE_GetREETTime                    | 实现不完整 |
