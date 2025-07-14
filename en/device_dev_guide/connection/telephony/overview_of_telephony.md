# Telephony Overview

\[ English | [简体中文](../../../../zh-cn/device_dev_guide/connection/telephony/overview_of_telephony.md) \]

## I. Background

Currently, openvela is widely used in various consumer terminal products. Some of these terminals, such as lightweight smart eSIM watches, require support for cellular communication functionality. To meet this demand, openvela needs to build a standardized, compatible, and sustainable openvela Telephony subsystem to manage core functions related to cellular communication and peripheral interfaces. This will further enrich and promote the development of the openvela ecosystem.

## II. Why Choose oFono as the Foundation

oFono is a Telephony Host Stack designed for Linux-based embedded mobile devices and desktop systems. It is licensed under the GPLv2 license. oFono is implemented using C language, GLib, and DBus, and supports various types of modems, such as:

- ATModem (AT command-based modem)
- RILModem (modem integrated with AOSP RIL format)
- ISIModem (integrated SIM modem)

Based on oFono's technical advantages and open-source ecosystem, openvela chooses oFono as the foundation to extend and develop the Telephony subsystem to meet cellular communication functionality requirements.

## III. Mobile Communication Solution

openvela integrates oFono into the system and enhances its mobile communication capabilities, such as supporting VoLTE (Voice over LTE) voice calls, thereby improving the mobile communication capabilities of the Internet of Things real-time operating system. Through hierarchical encapsulation and decoupling, as well as diversified chip platform integration methods, the overall mobile communication solution of the openvela system allows upper-layer applications (APPs) to achieve cross-platform reuse, providing users with the best communication experience.

Based on oFono as the service layer for Telephony, the system provides a TAPI (Telephony API) interface externally, while connecting to the RIL (Radio Interface Layer) at the lower layer to realize complete Telephony functionality.

![img](./figures/001.svg)

### 1. Telephony API (TAPI) Overview

#### TAPI Function Overview

TAPI is a DBus-based oFono D-Bus interface encapsulation layer, which mainly aims to:

1. Repackage all of oFono Stack’s D-Bus interfaces based on DBus Lib, making external applications unaware of D-Bus or oFono.
2. TAPI and oFono communicate based on a C/S architecture, with message distribution and subscription managed via D-Bus.

#### TAPI Architecture Diagram

Here is the architecture diagram for the Telephony API:

![img](./figures/002.svg)

#### TAPI Modular Design

TAPI is internally divided into multiple modules based on business functionality, with each module's functionality and code description as follows:

| **Module**                       | **File**                           | **Description**                        |
| :------------------------------- | :--------------------------------- | :------------------------------------- |
| Public API                       | `tapi_manager.c`<br>`tapi.h`       | Provides common Telephony API.         |
| Utility API                      | `tapi_utils.c/h`                   | Provides Telephony utility interfaces. |
| Call API                         | `tapi_call.c/h`<br>`tapi_ussd.c/h` | Call management interfaces.            |
| Network API                      | `tapi_network.c/h`                 | Network registration interfaces.       |
| Data API                         | `tapi_gprs.c/h`                    | Provides data service interfaces.      |
| SIM API                          | `tapi_sim.c/h`<br>`tapi_stk.c/h`   | SIM card management interfaces.        |
| SMS API                          | `tapi_sms.c/h`                     | SMS management interfaces.             |
| IMS API                          | `tapi_ims.c/h`                     | Provides IMS service interfaces.       |
| Provides IMS service interfaces. | `telephony_tools.c`                | Provides client simulation tools.      |

### 2. RIL Overview

#### RIL Function Overview

Telephony interacts with the modem (Modem) through the RIL mechanism. The Telephony layer communicates with the RILD process via a Socket, while the RILD process embeds the Vendor RIL to interact with the Modem.

#### RIL Design Principles

- AOSP Alignment: The openvela RIL interface references the design of Android 12 RIL AOSP.
    - oFono natively supports Android 4.3’s RIL interface, with parameters consistent with Android 4.3.
    - openvela selects and retains RIL parameters consistent with Android based on the Android 12 RIL interface for openvela's business requirements.
    - openvela does not support CDMA and NR5G-related interfaces defined by Android due to lack of business demand.
    - For IMS-related interfaces, openvela independently designs them according to its own needs, as there is no unified specification from AOSP.
    - openvela extends and customizes some interfaces according to business needs.
- Data Structure: Request and response parameters follow the Socket byte stream data structure definitions in oFono's source code gril/parcel.h.

### 3. Reference RIL Introduction

#### Reference RIL Functions

Reference RIL provides a reference implementation for QEMU Emulator, which simulates telephony functions such as calling, SMS, and internet access, making it convenient for debugging Telephony functions in QEMU emulators.

#### Reference RIL Module Division

Reference RIL divides the RIL module into two parts:

1. openvela LibRIL: The interface standard for openvela RIL.
2. Reference QEMU RIL: A reference implementation for the QEMU emulator.
Modem chip vendors can refer to the Reference QEMU RIL to implement Vendor RIL modules, which interact with the Modem for control-plane operations. In commercial products, openvela LibRIL and Vendor RIL together implement the complete RIL functionality.

## IV. Telephony Business Adaptation

To implement Telephony functionality on the openvela system, the following adaptation work must be completed:

- Cellular Application Layer APP: Call TAPI (Telephony API) interfaces to control and display the UI applications.
- Cellular Application Layer APP: Call TAPI (Telephony API) interfaces to control and display the UI applications.
- Cellular Data Plane: Adapt voice and data flow transmission logic.

The adaptation schemes for voice and data flows are described below.

### 1. Voice Adaptation

#### Voice Control Plane

The logical channel for the voice control plane is:

TAPI -> oFono voice -> RIL -> Modem

#### Voice Data Plane

The voice data plane directly interacts between the Modem and Audio DSP, handling the transmission, reception, and encoding/decoding of voice streams. Currently, Telephony supports the following voice functionalities:

- VoLTE voice on LTE IMS.
- CS voice on GSM and WCDMA.

The adaptation of the voice data plane requires chip vendors to develop openvela's audio drivers (Audio Driver).

### 2. Data Service

#### Data Control Plane

The control plane for data services is achieved via the following logical channel:

oFono gprs -> RIL -> Modem

In the data activation process, the Vendor RIL is responsible for creating the openvela OS network interface card and filling in information such as IP after receiving the IP information returned by the Modem. Currently, openvela’s cellular network interface card can be created in the following two ways:

1. Created in Vendor RIL.
2. Created in the openvela driver adaptation layer for the Modem chip vendor.

Chip vendors can choose the most suitable cellular network interface card adaptation scheme based on their needs.

#### Cellular Network Card Driver Implementation

The implementation of the cellular network card driver consists of the following two parts:

1. Modem hardware interaction: Responsible for data transmission and reception with the external world.
2. Network device structure implementation: Contains the callback functions required by the protocol stack and registers the structure with the protocol stack.

Efficient data transmission between these two modules needs to be implemented:

- The first part is handled by the Modem driver developer.
- The second part is related to the protocol stack.

#### Recommended Solution: TUN Virtual Network Card

A solution based on a TUN virtual network card is recommended. The features of this solution are as follows:

- Applicable scenarios: Suitable for scenarios where bandwidth requirements are not high and extreme network performance is not necessary.
- Performance limitations: May have performance bottlenecks.
- Ease of operation: User-space programs can directly invoke it, making it simple to operate.