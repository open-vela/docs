# Telephony 电话簿 API

SIM 卡电话簿管理接口，支持 ADN（普通电话簿）和 FDN（固定拨号号码）两类条目。

头文件：`#include <tapi_phonebook.h>`

## openvela 实现说明

- **ADN**：普通电话簿（Abbreviated Dialling Numbers），存储在 SIM 卡上的常规号码
- **FDN**：固定拨号号码（Fixed Dialling Numbers），启用后手机只能拨打 FDN 中的号码，受 PIN2 保护
- **FDN 操作需要 PIN2**：`insert_fdn_entry` / `delete_fdn_entry` / `update_fdn_entry` 调用时需要传入 PIN2
- **多卡支持**：所有接口带 `slot_id`
- **异步回调**：所有操作使用 `tapi_async_function` 异步返回结果

## ADN 电话簿

### tapi_phonebook_load_adn_entries

```c
int tapi_phonebook_load_adn_entries(tapi_context context, int slot_id, int event_id,
                                    tapi_async_function p_handle);
```

加载 SIM 卡上的 ADN 电话簿条目。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID，用于回调匹配。
- `p_handle` 异步回调函数，回调时返回 ADN 条目列表。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

## FDN 固定拨号

### tapi_phonebook_load_fdn_entries

```c
int tapi_phonebook_load_fdn_entries(tapi_context context, int slot_id, int event_id,
                                    tapi_async_function p_handle);
```

加载 SIM 卡上的 FDN 条目。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `p_handle` 异步回调函数，回调时返回 FDN 条目列表。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_phonebook_insert_fdn_entry

```c
int tapi_phonebook_insert_fdn_entry(tapi_context context, int slot_id, int event_id,
                                    char* name, char* number, char* pin2,
                                    tapi_async_function p_handle);
```

向 FDN 列表插入一条新条目（需要 PIN2 校验）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `name` 联系人姓名。
- `number` 电话号码。
- `pin2` SIM 卡 PIN2 码。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_phonebook_update_fdn_entry

```c
int tapi_phonebook_update_fdn_entry(tapi_context context, int slot_id, int event_id,
                                    int fdn_idx, char* new_name, char* new_number,
                                    char* pin2, tapi_async_function p_handle);
```

更新已有 FDN 条目（需要 PIN2 校验）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `fdn_idx` 要更新的条目索引。
- `new_name` 新的联系人姓名。
- `new_number` 新的电话号码。
- `pin2` SIM 卡 PIN2 码。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。

### tapi_phonebook_delete_fdn_entry

```c
int tapi_phonebook_delete_fdn_entry(tapi_context context, int slot_id, int event_id,
                                    int fdn_idx, char* pin2,
                                    tapi_async_function p_handle);
```

删除指定 FDN 条目（需要 PIN2 校验）。

**参数**：

- `context` Telephony 上下文句柄。
- `slot_id` SIM 卡槽 ID。
- `event_id` 事件 ID。
- `fdn_idx` 要删除的条目索引。
- `pin2` SIM 卡 PIN2 码。
- `p_handle` 异步回调函数。

**返回值**：

成功时返回 `0`，失败时返回负的错误码。
