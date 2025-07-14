# xxx Operation (Recommended Verb + Noun Form)

\[ English | [简体中文](../../../zh-cn/contribute/template/operation_guide-template.md) \]

> **Note:**  
>
> _1. This template provides recommended guidance for writing the operation guide document framework._  
>
> _2. All italic text represents writing guidance and should be removed from the final document._

**_【Overall Writing Requirements】_**

**_1. Identify the target audience:_** _Clearly identify the intended audience: developers/product managers/architects._  

**_2. Confirm content to include:_** _Introduce what the **feature/module** is (What), what it can do (Why), and how to operate it (How)._  

**_3. Adopt the user’s perspective:_** _From a developer’s viewpoint, provide the content that developers care about and need to use._  

**_4. Task-oriented writing:_** _Focus on the tasks developers need to complete, providing practical guidance._  

**_5. Do not be constrained:_** _Use this template as a reference; adjust flexibly based on actual needs._  

## Overview

_Required._

_Clearly define the basic information such as what and why to help developers establish an initial understanding of the feature/module._

_**【Developer Focus】**_

_What is this feature/module (definition – what)? What problem does it solve or what value does it bring (customer value – why)?_

_**【Writing Tips】**_

_Use scenario-based writing, employing the SCQA approach as follows:_

- _S: Situation – Introduce a scenario or fact that is familiar to everyone._  
- _C: Complication – The actual situation often conflicts with our requirements._  
- _Q: Question – How?_  
- _A: Answer – Our solution is ..._

**_【Writing Requirements】_**

- _Use only necessary terms, acronyms, or proprietary names, and provide explanations (linking to a glossary is also acceptable)._

## Prerequisites

_Required._

_List everything the user needs to do before executing the steps in this guide. It is recommended to use an **unordered list**._

## Prerequisite Concepts

_Optional._

_**【Developer Focus】**_

_What concepts must be understood before using this feature/module?_

**_【Writing Tips】_**

- _List the concepts developers should understand before using this guide._  
- _If concepts have complex logical relationships, consider adding diagrams for clarification._

**_【Writing Requirements】_**

- _Use only necessary terms, acronyms, or proprietary names, and provide explanations (linking to a glossary is also acceptable)._

## Implementation Principles

_Optional._

_**【Developer Focus】**_

_How does this feature/module work? Understanding its principles aids better usage._

**_【Writing Tips】_**

- _Prefer combining text and diagrams, such as flowcharts or architecture diagrams._  

- _Do not disclose confidential information._

**_【Writing Requirements】_**

- _Use only necessary terms, acronyms, or proprietary names, and provide explanations (linking to a glossary is also acceptable)._

## Usage Limitations

_Optional._

_**【Developer Focus】**_

_Are there any limitations when using this feature/module?_

**_【Writing Tips】_**

- _Describe limitations that may affect development. For example:_  
    - **_Functional Limitations_**  
        - _Unsupported usage scenarios._  
        - _Specification limits._

**_【Writing Example】_**

- _This feature is supported from version XXX and above._  

- _Each object must not exceed 100 KB._

## Environment Preparation

_Optional._

_Clearly state the development environment requirements (e.g., hardware requirements, software requirements, operating system requirements, etc.)._

## Operation Process

**_【Writing Tips】_**

_Optional._

- _What steps must developers follow to use this feature/module (How)?_  

- _Follow a layered structure: Scenario (task scenario) → Task logic (operation flow) → Operation steps (step by step)._  

- _If there are many operation steps, provide a flowchart._

## Operation Steps

**_【Writing Requirements】_**

_Required._

- _**Each step should clearly specify the executor (who), the purpose (why), the operation (what/how), and the context (when/where). Use imperative sentences to describe the steps.**_  

- _Ensure any sample code is executable._  

- _After completion, provide guidance on how to confirm successful execution._  

- _Mask sensitive information such as phone numbers, ID numbers, or account names (e.g., 186********) and use private IP addresses or generic domain names (e.g., xx.xx.xx.xx, www.example.com); **do not use real IP addresses or domain names**._

## FAQs

_Optional._

**_【Developer Focus】**_

_Common issues developers may encounter during the operation process._

**_【Writing Tips】_**

_Describe various issues that may be encountered during the operation process and their solutions to improve development efficiency._

_Refer to the [FAQ template](./faq_template.md) for writing guidelines._

## Next Steps

**_【Writing Tips】_**

_Use an unordered list (no more than 5 items) to suggest topics developers may be interested in exploring next._