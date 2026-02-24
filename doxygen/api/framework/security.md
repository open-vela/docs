
# Vela Security Framework API

## 一、MiTEE CA 应用级API接口
### 1. 通用安全存储SST CA API
主要是对安全存储/sst分区的读写操作，实现位于：vendor/xiaomi/mitee_iot/ca/comsst

```
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
 
### 2. 三元组CA API
主要是对于设备三元组中的did和key读写操作，实现位于：
vendor/xiaomi/mitee_iot/ca/triad

```
int triad_store_did(uint8_t* did, uint16_t len);
int triad_load_did(uint8_t* did, uint16_t len);
int triad_store_key(uint8_t* key, uint16_t len);
int triad_load_key(uint8_t* key, uint16_t len);
int triad_get_hmac(uint8_t* input, uint16_t inlen,
uint8_t* output, uint16_t outlen);
```
 

### 3. 微信支付CA API
主要是对于微信安全支付相关读写操作，实现位于：vendor/xiaomi/mitee_iot/ca/wxcodepay

```
uint32_t wxcodepay_tee_data_read(int item, uint8_t* buff, uint32_t* out_len);
uint32_t wxcodepay_tee_data_write(int item, const uint8_t* buf, uint32_t len);
uint32_t wxcodepay_tee_data_delete(int item);
bool is_wxcodepay_tee_data_exited(int item);
```
 


### 4. 支付宝支付CA API
主要是对于支付宝安全支持相关读写操作，实现位于：vendor/xiaomi/mitee_iot/ca/alipay

```
uint32_t alipay_tee_data_read(const char* item_name, uint8_t* buff,
uint32_t* out_len);
uint32_t alipay_tee_data_write(const char* item_name, const uint8_t* buf,
uint32_t len);
uint32_t alipay_tee_data_delete(const char* item_name);
bool is_alipay_tee_data_exited(const char* item_name);
```
 

### 5. 普通PIN码CA API
主要是对于普通PIN码读写操作，实现位于：vendor/xiaomi/mitee_iot/ca/pin

```
uint32_t pin_store(bool is_deletable, uint8_t *buff, uint32_t len);
bool pin_is_exist(bool is_deletable);
uint32_t pin_delete(bool is_deletable);
uint32_t pin_verify(bool is_deletable, uint8_t *buff, uint32_t len);
uint32_t pin_change(bool is_deletable, uint8_t *old, uint32_t oldlen,
uint8_t *new, uint32_t newlen);
uint32_t pin_getsha256(bool is_deletable, uint8_t *buff, uint32_t len);
```
 

## 二、MiTEE Rootkey API接口
### 1. 读取rootkey
位于TEE OS里的tee server miteed会通过如下接口获取rootkey：

```
#include <sys/boardctl.h>
 boardctl(BOARDIOC_UNIQUEKEY, tmp_key);
```
 
### 2. 写入rootkey
rootkey生成写入只在工厂版本中TEE OS系统第一次启动时做rootkey_provision，对应工厂程序位于：vendor/xiaomi/miwear/factest/rootkey_provision

```
norflash_api_security_register_erase(HAL_FLASH_ID_0, 2048, 32)
norflash_api_security_register_write(HAL_FLASH_ID_0, 2048, rn, 32)
norflash_api_security_register_lock(HAL_FLASH_ID_0, 2048, 32)
```
 
## 三、mitee_iot框架层API接口
mitee_iot框架层主要包括两部分内容，
其一是TEE Client部分(libteec)，主要实现部分GP TEE client API（根据潜在的需求，可能会全部实现）
另外是TEE Server部分(miteed)，主要是接收和处理CA发起的TEE Client请求，实现GP TEE Internal API
注：TEE Client与TEE Server之间是采用rpmsg socket进行数据交换
TEE Client API

a. TEEC_InitializeContext
描述：
This function initializes a new TEE Context, forming a connection between this Client Application and the TEE identified by the string identifier name.
```
/**
 * TEEC_InitializeContext() - Initializes a context holding connection
 * information on the specific TEE, designated by the name string.
 
* @param name A zero-terminated string identifying the TEE to connect to.
 * If name is set to NULL, the default TEE is connected to. NULL
 * is the only supported value in this version of the API
 * implementation.
 *
 * @param context The context structure which is to be initialized.
 *
 * @return TEEC_SUCCESS The initialization was successful.
 * @return TEEC_Result Something failed.
 */
 TEEC_Result TEEC_InitializeContext(const char *name, TEEC_Context *context);
```
 
b. TEEC_FinalizeContext
描述：
This function finalizes an initialized TEE Context, closing the connection between the Client Application and the TEE.
```
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
 
c. TEEC_OpenSession
描述：
This function opens a new Session between the Client Application and the specified Trusted Application.
```
/**
 * TEEC_OpenSession() - Opens a new session with the specified trusted
 * application.
 *
 * @param context The initialized TEE context structure in which
 * scope to open the session.
 * @param session The session to initialize.
 * @param destination A structure identifying the trusted application
 * with which to open a session.
 *
 * @param connectionMethod The connection method to use.
 * @param connectionData Any data necessary to connect with the chosen
 * connection method. Not supported, should be set to
 * NULL.
 * @param operation An operation structure to use in the session. May
 * be set to NULL to signify no operation structure
 * needed.
 *
 * @param returnOrigin A parameter which will hold the error origin if
 * this function returns any value other than
 * TEEC_SUCCESS.
 *
 * @return TEEC_SUCCESS OpenSession successfully opened a new session.
 * @return TEEC_Result Something failed.
 *
 */
 TEEC_Result TEEC_OpenSession(TEEC_Context *context,
 TEEC_Session *session,
 const TEEC_UUID *destination,
 uint32_t connectionMethod,
 const void *connectionData,
 TEEC_Operation *operation,
 uint32_t *returnOrigin);
```
 
d. TEEC_CloseSession
描述：
This function closes a Session which has been opened with a Trusted Application.
```
/**
 * TEEC_CloseSession() - Closes the session which has been opened with the
 * specific trusted application.
 *
 * @param session The opened session to close.
 */
 void TEEC_CloseSession(TEEC_Session *session);
 
```

e. TEEC_InvokeCommand
描述：
This function invokes a Command within the specified Session.
```
/**
 * TEEC_InvokeCommand() - Executes a command in the specified trusted
 * application.
 *
 * @param session A handle to an open connection to the trusted
 * application.
 * @param commandID Identifier of the command in the trusted application
 * to invoke.
 * @param operation An operation structure to use in the invoke command.
 * May be set to NULL to signify no operation structure
 * needed.
 * @param returnOrigin A parameter which will hold the error origin if this
 * function returns any value other than TEEC_SUCCESS.
 *
 * @return TEEC_SUCCESS OpenSession successfully opened a new session.
 * @return TEEC_Result Something failed.
 */
 TEEC_Result TEEC_InvokeCommand(TEEC_Session *session,
 uint32_t commandID,
 TEEC_Operation *operation,
 uint32_t *returnOrigin);
```
 
g. TEEC_AllocateSharedMemory
描述：
This function allocates a new block of memory as a block of Shared Memory within the scope of the specified TEE Context, in accordance with the parameters which have been set by the Client Application inside the sharedMem structure.
```
/**
 * TEEC_AllocateSharedMemory() - Allocate shared memory for TEE.
 *
 * @param context The initialized TEE context structure in which scope to
 * open the session.
 * @param sharedMem Pointer to the allocated shared memory.
 *
 * @return TEEC_SUCCESS The registration was successful.
 * @return TEEC_ERROR_OUT_OF_MEMORY Memory exhaustion.
 * @return TEEC_Result Something failed.
 */
 TEEC_Result TEEC_AllocateSharedMemory(TEEC_Context *context,
 TEEC_SharedMemory *sharedMem);
```
 
h. TEEC_ReleaseSharedMemory
描述：
This function deregisters or deallocates a previously initialized block of Shared Memory.
```
/**
 * TEEC_ReleaseSharedMemory() - Free or deregister the shared memory.
 *
 * @param sharedMem Pointer to the shared memory to be freed.
 */
 void TEEC_ReleaseSharedMemory(TEEC_SharedMemory *sharedMemory);
```
 

GP Internal API目前TEE Server 上支持GP internal API列表具体情况：

|编号  |函数  |状态  |描述  |
| --- | --- | --- | --- |
|  | TA_CreateEntryPoint |支持 |  |
|  | TA_DestroyEntryPoint |支持  |  |
|  | TA_OpenSessionEntryPoint |支持  |  |
|  | TA_CloseSessionEntryPoint |支持  |  |
|  | TA_InvokeCommandEntryPoint |支持  |  |
|  |  |  |  |
|  |TEE_OpenTASession |实现不完整  |  |
|  |TEE_CloseTASession|实现不完整  |  |
|  |TEE_InvokeTACommand |实现不完整  |  |
|  |  |  |  |
|  |TEE_CheckMemoryAccessRights |实现不完整  |  |
|  |  |  |  |
|  |TEE_Malloc|支持  |  |
|  |TEE_Realloc|支持  |  |
|  |TEE_Free|支持  |  |
|  |TEE_MemMove|支持  |  |
|  |TEE_MemCompare|支持  |  |
|  |TEE_MemFill|支持  |  |
|  |  |  |  |
|  |TEE_GetObjectInfo1 |支持  |  |
|  |TEE_CloseObject| 支持 |  |
|  |TEE_AllocateTransientObject |支持  |  |
|  |TEE_FreeTransientObject |支持  |  |
|  |TEE_ResetTransientObject |支持  |  |
|  |TEE_PopulateTransientObject | 支持 |  |
|  |TEE_InitRefAttribute | 支持 |  |
|  |TEE_InitValueAttribute |支持  |  |
|  |TEE_CopyObjectAttributes1 |支持  |  |
|  |TEE_GenerateKey| 实现不完整 |  |
|  | |  |  |
|  |TEE_OpenPersistentObject|实现不完整  |  |
|  |TEE_CreatePersistentObject|实现不完整  |  |
|  |TEE_CloseAndDeletePersistentObject|实现不完整  |  |
|  |TEE_RenamePersistentObject|实现不完整  |  |
|  | |  |  |
|  |TEE_ReadObjectData |实现不完整  |  |
|  |TEE_WriteObjectData |实现不完整  |  |
|  |TEE_TruncateObjectData |实现不完整  |  |
|  |TEE_SeekObjectData |实现不完整  |  |
|  | |  |  |
|  |TEE_AllocateOperation| 支持 |  |
|  |TEE_FreeOperation| 支持 |  |
|  |TEE_GetOperationInfo| 支持 |  |
|  |TEE_GetOperationInfoMultiple| 支持 |  |
|  |TEE_ResetOperation| 支持 |  |
|  |TEE_SetOperationKey| 支持 |  |
|  |TEE_SetOperationKey2| 支持 |  |
|  |TEE_CopyOperation| 支持 |  |
|  |TEE_DigestUpdate| 支持 |  |
|  |TEE_DigestDoFinal| 支持 |  |
|  |TEE_CiperInit| 支持 |  |
|  |TEE_CiperUpdate| 支持 |  |
|  |TEE_CiperDoFinal| 支持 |  |
|  |TEE_MACInit| 支持 |  |
|  |TEE_MACUpdatel| 支持 |  |
|  |TEE_MACComputeFinal| 支持 |  |
|  |TEE_MACCompareFinal| 支持 |  |
|  | |  |  |
|  |TEE_AEInit|实现不完整  |  |
|  |TEE_AEUpdateAAD|实现不完整  |  |
|  |TEE_AEUpdate|实现不完整  |  |
|  |TEE_AEEncrypt|实现不完整  |  |
|  |TEE_AEDecrypt|实现不完整  |  |
|  |TEE_AsymmetricEncrypt|实现不完整  |  |
|  |TEE_AsymmetricDecrypt|实现不完整  |  |
|  |TEE_AsymmetricSignDigest|实现不完整  |  |
|  |TEE_AsymmetricVerifyDigest|实现不完整  |  |
|  | |  |  |
|  |TEE_DeriveKey|实现不完整  |  |
|  | |  |  |
|  |TEE_GenerateRandom|实现不完整  |  |
|  | |  |  |
|  |TEE_GetSystemTime|实现不完整  |  |
|  |TEE_GetTAPersistentTime|实现不完整  |  |
|  |TEE_SetTAPersistentTime|实现不完整  |  |
|  |TEE_GetREETTime|实现不完整  |  |
