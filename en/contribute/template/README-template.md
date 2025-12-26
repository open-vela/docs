# xxx System/Module

\[ English | [简体中文](../../../zh-cn/contribute/template/README-template.md) \]

> **Note:**
>
> _1. This template provides recommended guidance for writing a README._
>
> _2. All italics are writing guides; please ensure they are all deleted in the formal document._

**_【General Writing Requirements】_**

**_1. Confirm the Writing Content:_**_Introduce what the **system/module** is (What), what it can do (Why), and how to develop it (How)._ 

**_2. Adopt the User's Perspective:_**_Present content from the developer's perspective, focusing on what they care about and need to use._ 

**_3. Be Flexible:_**_The template is for reference only; adjust it flexibly according to the actual situation._ 

## Overview

_【Writing Requirement】**Required**_

_**Content Introduction:** The role of this system/module in the entire openvela architecture, the functions it implements, usage scenarios, and supported devices._

_**Notes:**_

| Item  | Content Requirement                                                                                                                                        |
| ----- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **1** | **Language Requirements**                                                                                                                                  |
| 1.1   | Writing style: Formal language, avoiding colloquial expressions.                                                                                           |
| 1.2   | Compliance requirements: Do not use words with legal and compliance risks, such as third - party intellectual property - specific concepts.                |
| 1.3   | Consistent terminology: Ensure consistency with the terminology library, and provide the full form of abbreviations on their first appearance in the text. |
| **2** | **Format Requirements**                                                                                                                                    |
| 2.1   | Correct punctuation, with sentences ending in periods.                                                                                                     |
| 2.2   | Present content in bullet points or categorized lists as much as possible.                                                                                 |
| 2.3   | For supplementary explanations of content, use styles like "Note/Attention/Warning".                                                                       |
| **3** | **Tables**                                                                                                                                                 |
| 3.1   | Tables must have headers, and empty cells should be filled with "Not Applicable/None".                                                                     |
| **4** | **Screenshots**                                                                                                                                            |
| 4.1   | Graphics should be logically clear and used in conjunction with text.                                                                                      |
| 4.2   | It is recommended to use the.png format.                                                                                                                   |
| 4.3   | Use Chinese for Chinese - language figures and English for English - language figures.                                                                     |

## Architecture Diagram

_【Writing Requirement】**Optional**_

| Item | Content Requirement                                                                                                                      |
| ---- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| 1    | Use an architecture diagram to illustrate the system/module architecture and provide necessary explanations of the main components.      |
| 2    | If this module is part of a subsystem, indicate that understanding the subsystem - related concepts is required and provide a reference. |

## Code Directory

_【Writing Requirement】**Required**. Clarify the code directory structure of this project and the functional description of each directory._

```tree
├── include                 # Framework code
│   ├── tapi_call.h         # Header file directory
│   ├── tapi_cbs.h
├── src
│   ├── tapi_call.c
│   ├── tapi_cbs.c
│   └── tapi_utils.c        # Utility class
├── tools
│   └── telephony_tool.c
```

## Usage Restrictions

_【Writing Requirement】**Optional**. Specify the prerequisites for running the subsystem, such as a specific fixed version of the operating system._

| Item | Content Requirement                                |
| ---- | -------------------------------------------------- |
| 1    | Clarify functional or operational restrictions.    |
| 2    | Constraints that impact task - guided development. |

## Development Guide

_【Writing Requirement】**Optional**_

| Item  | Content Requirement                                                                              |
| ----- | ------------------------------------------------------------------------------------------------ |
| **1** | **How to Write Good Steps**                                                                      |
| 1.1   | Step completeness: Provide all necessary steps to ensure successful completion of the operation. |
| 1.2   | Task sentences: Use the "verb + noun" structure.                                                 |
| 1.3   | Clear purpose: Specify the purpose of each step, i.e., the desired goal.                         |
| 1.4   | Include success criteria after step completion.                                                  |
| **2** | **How to Write Good Code Segments**                                                              |
| 2.1   | Ensure the code is correct and executable.                                                       |
| 2.2   | Add clear comments for critical steps.                                                           |

## Interface Description

_【Writing Requirement】**Optional**. Provide links to API interfaces in this repository._

## Related Repositories

_【Writing Requirement】**Optional**. List links to strongly related repositories for further learning by developers._
