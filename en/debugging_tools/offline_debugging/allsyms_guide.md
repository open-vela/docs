# Allsyms Symbol Table Feature Usage Guide

\[ English | [简体中文](../../../zh-cn/debugging_tools/offline_debugging/allsyms_guide.md) \]

This document provides guidance on enabling and using the **Allsyms** feature in the openvela system. By enabling this feature, you can compile a complete symbol table into the firmware image, enabling the system to resolve function addresses into human-readable function names during runtime. This enhances on-device debugging efficiency, especially for analyzing crash stacks.

## I. Prerequisites

Before compiling firmware that includes the **Allsyms** feature, you must ensure the following Python packages are installed in your development environment. The build system uses these tools to parse **ELF** files and generate the symbol table.

Run the following command in your terminal to install them:

```C
pip3 install pyelftools cxxfilt
```

## II. How to Enable Allsyms

> **Warning**
>
> Enabling the **Allsyms** feature significantly increases the size of the final firmware image. Please evaluate your storage capacity and enable this feature only in debug builds.

To enable this feature, add the following configuration option to your project's configuration file:

```Makefile
CONFIG_ALLSYMS=y
```

The underlying implementation for this feature is located at the following path in openvela:

`nuttx/libs/libc/symtab`

## III. Usage

After enabling **Allsyms**, you can utilize the symbol table for debugging in the following ways.

### 1. Automatically Display Function Names in Backtraces

This is the primary use case for **Allsyms**. When the system crashes or you manually call functions like `dumpstack` or `sched_dumpstack`, the printed backtrace will no longer show raw addresses. Instead, it will display the resolved function names, helping you to locate issues quickly.

### 2. Format Symbol Output in `printf`

You can use the `%pS` format specifier in `printf-family` functions to directly print the symbol information corresponding to a specific address. If a matching symbol is not found, the system will print the original address.

**Code Example:**

```C
#include <stdio.h>
extern void hello_world(void);
void my_debug_function(void)
{
  // Print the symbol name and address of the hello_world function
  printf("Symbol info for hello_world: %pS\n", hello_world);
}
```

### 3. Manually Query Symbols Using APIs

openvela provides two core APIs that allow you to convert between function names and addresses in your code:

- `allsyms_findbyname()`: Finds the address of a function based on its name.
- `allsyms_findbyvalue()`: Finds the closest function name based on an address.

## IV. API Reference

The following are the core data structures and function prototypes related to the **Allsyms** feature.

### 1. `struct symtab_s`

This structure defines a single entry in the symbol table.

```C
/* struct symbtab_s describes one entry in the symbol table.  A symbol table
 * is a fixed size array of struct symtab_s. The information is intentionally
 * minimal and supports only:
 *
 * 1. Function pointers as sym_values.  Of other kinds of values need to be
 *    supported, then typing information would also need to be included in
 *    the structure.
 *
 * 2. Fixed size arrays.  There is no explicit provisional for dynamically
 *    adding or removing entries from the symbol table (realloc might be
 *    used for that purpose if needed).  The intention is to support only
 *    fixed size arrays completely defined at compilation or link time.
 */

struct symtab_s
{
  FAR const char *sym_name;  /* A pointer to the symbol name string */
  FAR const void *sym_value; /* The value associated with the string */
};
```

### 2. `allsyms_findbyname()`

Finds a symbol table entry by its name.

```C
/****************************************************************************
 * Name: allsyms_findbyname
 *
 * Description:
 *   Find the symbol in the symbol table with the matching name.
 *
 * Returned Value:
 *   A reference to the symbol table entry if an entry with the matching
 *   name is found; NULL is returned if the entry is not found.
 *
 ****************************************************************************/

FAR const struct symtab_s *allsyms_findbyname(FAR const char *name,
                                              FAR size_t *size);
```

### 3. `allsyms_findbyvalue()`

Finds a symbol table entry by its value (address).

```C
/****************************************************************************
 * Name: symtab_findbyvalue
 *
 * Description:
 *   Find the symbol in the symbol table whose value closest (but not greater
 *   than), the provided value. This version assumes that table is not
 *   ordered with respect to symbol value and, hence, access time will be
 *   linear with respect to nsyms.
 *
 * Returned Value:
 *   A reference to the symbol table entry if an entry with the matching
 *   name is found; NULL is returned if the entry is not found.
 *
 ****************************************************************************/

FAR const struct symtab_s *allsyms_findbyvalue(FAR void *value,
                                               FAR size_t *size);
```

## V. FAQ

### 1. Compile-time error indicates missing `elftools` or `cxxfilt` modules

#### Problem Description

![img](./figures/001.jpg)

#### Cause Analysis

This error occurs because the build process for the **Allsyms** feature relies on these two Python tools to process **ELF** files and extract symbol information.

#### Solution

Please refer to the [Prerequisites](#prerequisites) section of this document and use the `pip3` command to install them.

## VI. Related Documents

- [Backtrace Usage Guide](./backtrace.md)
