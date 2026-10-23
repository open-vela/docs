# Quick App Development Guide (AI Workflow)

\[ English | [简体中文](../../../zh-cn/app_dev/quickapp/quickapp_ai_workflow.md) \]

> This guide is for developers. It shows how to use the openvela quick app workflow to automate the whole development flow, from requirements to code to debugging.

## I. Overview

### 1. What Is a Quick App

A quick app is a lightweight app that runs on openvela devices (watches, bands, speakers, AI hardware and so on) and is developed with a front-end tech stack (HTML/CSS/JavaScript).

### 2. Technical Features

| Feature              | Description                                                                                    |
| -------------------- | ---------------------------------------------------------------------------------------------- |
| Web-like development | Pages use a three-part `template` + `style` + `script` structure                               |
| Built-in components  | Native components such as `div`, `text`, `image` and `list`                                    |
| Flex layout          | Flexbox layout by default                                                                      |
| System capabilities  | System APIs for network requests, sensors, recording, vibration, Bluetooth and more            |
| Multi-device support | One codebase for different screen sizes (round and square watch screens, 7-inch screens, etc.) |

### 3. Use Cases

- Lightweight apps on smart watches and bands
- Interactive UIs for smart speakers with screens
- Control panels for AI hardware
- Configuration and display UIs for IoT devices

### 4. Workflow Overview

The workflow splits development into four stages, each handled by an AI in a different role:

| Stage | Name                | AI role            | Output                    |
| ----- | ------------------- | ------------------ | ------------------------- |
| S1    | PRD generation      | AI product manager | 01-prd.md                 |
| S2    | Technical design    | AI architect       | 02-tech-design.md         |
| S3    | Feature development | AI engineer        | Project code files        |
| S4    | Emulator debugging  | AI test engineer   | Debug report + fixed code |

> The workflow supports two modes: full mode (S1→S2→S3→S4, for when the requirements are unclear) and quick mode (skips S1/S2 and generates code directly, for when the requirements are clear).

## II. Environment Setup

> **Environment requirements**
> - Operating system: **Ubuntu 22.04** is recommended
> - Windows Subsystem for Linux (WSL) and Docker container environments are **not supported**

### Step 1: Install Node.js

Node.js v22 or a later LTS version is recommended. On Ubuntu 22.04, nvm is the recommended way to manage versions:

```bash
# 1. Install nvm (using the current latest version, v0.40.4)
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.4/install.sh | bash

# 2. Reopen the terminal and install Node 22 (LTS)
nvm install 22

# 3. Verify
node -v
npm -v
```

### Step 2: Install the adb Tool

Deploying a quick app to the openvela emulator requires adb (Android Debug Bridge) to push files. The openvela repository doesn't ship adb, so install it manually:

```bash
sudo apt install -y adb
```

### Step 3: Install the AIoT IDE

Download: https://iot.mi.com/vela/quickapp/zh/guide/start/use-ide.html

### Step 4: Configure the LLM

The workflow calls the LLM through Claude Code. The officially recommended model is MiMo, and this section uses MiMo as the configuration example.

- **Use the multimodal model mimo-v2.5. Don't use mimo-v2.5-pro.**
- **Configure it by following the official documentation**: https://platform.xiaomimimo.com/docs/zh-CN/integration/claudecode
- **Make sure all four model fields in ~/.claude/settings.json are set to mimo-v2.5** (this prevents an automatic switch to pro while running):

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "<your MiMo base URL>",
    "ANTHROPIC_AUTH_TOKEN": "<your API key>",
    "ANTHROPIC_MODEL": "mimo-v2.5",
    "ANTHROPIC_DEFAULT_SONNET_MODEL": "mimo-v2.5",
    "ANTHROPIC_DEFAULT_OPUS_MODEL": "mimo-v2.5",
    "ANTHROPIC_DEFAULT_HAIKU_MODEL": "mimo-v2.5"
  }
}
```

### Step 5: Install the IDE Plugin

Install the following IDE plugin from the plugin marketplace:

| Plugin                  | Purpose                 |
| ----------------------- | ----------------------- |
| Claude Code for VS Code | AI-assisted development |

## III. Creating and Starting a Project

### Step 1: Download the Workflow Template

Open a terminal in an empty folder and run:

```bash
npx create-vela-workflow my-app --mode claude
```

### Step 2: Open the Project in the AIoT IDE

Open the downloaded `my-app` in the AIoT IDE. It contains a `.claude` folder.

### Step 3: Create the Project and Generate Code with the AI Workflow

1. In the AIoT IDE, open the Claude Code plugin and enter `/vela-workflow` in the Claude Code chat box. Follow the prompts to generate a complete quick app. For example, enter: "Create a music player quick app for Xiaomi Watch that supports play/pause, previous/next track and a progress bar".

2. After the workflow starts, the interaction goes like this:

```
Step 1.1  Confirm requirements  → enter y to confirm / e to edit
Step 1.2  Confirm design draft  → enter 1 to provide a design draft / 2 to skip
Step 1.3  Choose mode           → enter 1 for the full workflow / 2 for quick mode
```

You can also create a project manually by following the [official documentation (Chinese)](https://iot.mi.com/vela/quickapp/zh/guide/start/use-ide.html) and write the code by hand.

### Step 4: Configure the Emulator

1. Once you have the code, open the generated code project in the AIoT IDE.
2. In the AIoT IDE, click the "Emulator" button in the banner bar.
3. Click "New" and select the **vela-watch-5** image.
4. Enter an emulator name and click "New".

### Step 5: Debug in the Emulator

Configure it by following https://www.npmjs.com/package/velajs-mcp. Once it is configured, tell the AI "**Use VelaJS MCP to start the xxx emulator and run the project**" to enter the emulator debugging stage.

> Before release, it's recommended to run and validate the app on the openvela emulator to make sure it works in a real system environment. This step uses the AIoT IDE built-in emulator, which differs from the openvela emulator. For how to deploy to and validate on the openvela emulator, see the [deploying to the openvela emulator section of Quick App Development Guide (Manual Development)](./quickapp_manual.md#iv-deploying-to-the-openvela-emulator).

## IV. Packaging

See [Section III, Packaging, of Quick App Development Guide (Manual Development)](./quickapp_manual.md#iii-packaging). **You can use the workflow to assist development.**

## V. Deploying to the openvela Emulator

See [Quick App Development Guide (Manual Development)](./quickapp_manual.md#iv-deploying-to-the-openvela-emulator).

## VI. Deploying to a Development Board

See [Quick App Development Guide (Manual Development)](./quickapp_manual.md#v-deploying-to-a-development-board).

## VII. FAQ

### 1. Usage

**Q: How do I resume an interrupted workflow?**

Enter `/vela-workflow` again. The system detects the unfinished session and offers to resume it.

**Q: How do I choose between quick mode and full mode?**

- **Full mode**: when the requirements are unclear, you need documentation, or a team is collaborating
- **Quick mode**: when the requirements are clear, you want a quick prototype, or you are developing alone

**Q: What if the VelaJS MCP tools are unavailable?**

1. Make sure the aiot-core, aiot-emulator and aiot-devtools plugins are installed
2. Restart the IDE and try again
3. Check that the paths in the MCP configuration are correct

**Q: What if the generated code has problems?**

- At a checkpoint, enter `e` and describe the problem; the AI iterates on a fix
- Enter S4 emulator debugging, where the AI finds and fixes runtime problems automatically

**Q: Which devices are supported?**

Quick apps target smart wearables based on VelaOS:
- Xiaomi Watch S1 Pro / S5 (480x480px round screen)
- Xiaomi Watch S3 / S4 / H1 (466x466px round screen)
- REDMI Watch 5 (432x514px square screen)
- Xiaomi Smart Band 9 (192x490px racetrack screen)
- Other devices based on the Vela system

### 2. Common Layout and Style Issues

- If the layout is broken, add `flex-direction:column;` to the root component's style
- If the content of a `list` doesn't show, give the `list-item` style an explicit width and height:
  ```css
  height:50px;
  width:100%;
  ```

## Appendix

### 1. Workflow Usage Examples

**Example 1: Quickly create a timer app**

```
Create a timer quick app for Xiaomi Watch with:
- Start/pause/reset
- A minutes:seconds:milliseconds display
- A circular progress ring
```

Choose quick mode → the AI generates the code directly → review and confirm → start emulator debugging

**Example 2: Create an app from a design draft**

```
Create an app store for Xiaomi Watch, design draft: https://www.figma.com/board/xxx/store?node-id=2-1621
```

Choose full mode → the AI generates the PRD → technical design → exports assets from Figma and generates code → emulator debugging

**Example 3: Add a new page to an existing project**

```
Add a playlist page to the current project that lists songs and plays one when tapped
```

The AI detects the existing project → incremental development mode → adds the page and route → updates the manifest

### 2. VelaJS MCP Tool Reference

#### Device and Debug Management

| Function                                            | AI prompt                                    |
| --------------------------------------------------- | -------------------------------------------- |
| List available emulators                            | Show me the installed emulator devices       |
| List connected devices (emulators and real devices) | List the connected devices for me            |
| Select the debug device                             | Set the target device                        |
| Start debugging                                     | Build and push the app to the device         |
| Stop debugging                                      | Stop the current debug session               |
| Get debug status                                    | Check whether debugging is currently running |
| Build the project                                   | Build the rpk package                        |

#### UI Inspection Tools

| Function            | AI prompt                                         |
| ------------------- | ------------------------------------------------- |
| Take a screenshot   | Get a screenshot of the current page UI           |
| Get a page snapshot | Get the full component tree                       |
| Get element info    | Show the attributes and styles of a given element |

#### Logging and Debugging Tools

| Function             | Description                                 |
| -------------------- | ------------------------------------------- |
| Get console logs     | View the JS console output                  |
| Get network requests | View the fetch request history              |
| Run a script         | Evaluate a JS expression in the app context |
| Get storage data     | View localStorage data                      |
| Get build logs       | View the build output                       |
| Get emulator logs    | View the emulator system logs               |

#### Using It Outside the Workflow

Even without starting the full workflow, you can ask for VelaJS MCP capabilities directly in the chat:
- "Use Vela js-mcp to start the emulator and debug the current project"
- "Take a screenshot of the current page and check whether the layout is correct"
- "Check the console logs for errors"
- "Simulate a tap on the play button on the page"

### 3. Figma MCP Design Integration (Optional)

When you have a Figma design, the workflow fetches the design data automatically through Figma MCP, so that the code closely matches the design.

#### Configuration

Add the Figma server to the MCP configuration:

```json
{
  "mcpServers": {
    "figma": {
      "command": "uvx",
      "args": ["mcp-figma"],
      "env": {
        "FIGMA_ACCESS_TOKEN": "your Figma token",
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "autoApprove": ["get_file", "get_file_nodes", "export_image"]
    }
  }
}
```

To get a token: Figma → Settings → Personal Access Tokens → create a new token.

#### Usage

At the Step 1.2 design-draft confirmation, choose `1` and paste the Figma link. Supported URL formats:

```
https://www.figma.com/board/{file_key}/{name}?node-id={node_id}
https://www.figma.com/file/{file_key}/{name}?node-id={node_id}
```

The workflow parses the link, fetches the node structure and styles, exports image assets into the project directory, and generates code from the real design data.

#### How the Two MCPs Divide the Work

| MCP tool   | Purpose                                       | Stage                                |
| ---------- | --------------------------------------------- | ------------------------------------ |
| Figma MCP  | Get design information, export images         | S1/S2/S3 (design-driven development) |
| VelaJS MCP | Run and debug, screenshots, interaction tests | S4 (emulator debugging)              |

> Don't mix them up. Use Figma MCP during the design stages and VelaJS MCP during debugging.
