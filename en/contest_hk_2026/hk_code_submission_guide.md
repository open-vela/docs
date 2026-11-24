# Code Submission Guide for the Hong Kong University Track
\[ English | [简体中文](../../zh-cn/contest_hk_2026/hk_code_submission_guide.md) | [繁體中文](../../zh-cn/contest_hk_2026/hk_code_submission_guide_zh-hk.md) \]

> This guide is for university-track teams that use openvela in the 《三十港章 慧智北都》 AIoT competition. It explains how to submit your application code to openvela's GitHub repositories: fork the target repository first, then open a Pull Request (PR) against it.

## I. Which Repository to Submit To

The target branch of every PR is `dev-ai-contest-2026`.

| What you submit | Target repository | Notes |
| --------------- | ----------------- | ----- |
| Quick App (JS app) | [`open-vela/packages_apps`](https://github.com/open-vela/packages_apps) | Quick Apps that run on the openvela emulator |
| Native app (C) | [`open-vela/packages_demos`](https://github.com/open-vela/packages_demos) | The openvela native application examples repository |
| Board configuration, peripheral drivers, and other board-related changes | [`open-vela/vendor_allwinnertech`](https://github.com/open-vela/vendor_allwinnertech) | The board support code of the R528 MIBOX-X1 is in this repository |
| Changes to common repositories such as `nuttx` | The matching common repository | Also fork it and open a PR against `dev-ai-contest-2026` |

Note: the Quick Apps in [`packages_fe_examples`](https://github.com/open-vela/packages_fe_examples) only run in the emulator built into AIoT-IDE and are for reference only. Do not submit your project there.

## II. Before You Start

- Have a GitHub account.
- Finish setting up the development environment, so that you can fetch the code, build it, and run it. See the [Development Guide](./hk_university_track_dev_guide.md) and [Quick Start (Ubuntu)](../quickstart/openvela_ubuntu_quick_start.md).
- A Quick App must run on the openvela emulator first. See Chapter IV of the [Quick App Development Guide](../app_dev/quickapp/quickapp_manual.md).
- A native app must build and run on the development board or the emulator first. For the board, see the [Development Board Guide](./mibox_x1_board_guide.md).
- Sign the Contributor License Agreement (CLA). The first PR you open is checked automatically, and a PR cannot be merged until the CLA is signed. Sign it on the [openvela website](https://openvela.com/#/community/cla) with your GitHub account. After signing, you do not need to recreate the PR. Comment `/check-cla` on the existing PR to trigger the check again.

## III. Steps

The example below uses a Quick App. A native app works the same way: use the `packages_demos` repository and the `packages/demos` directory.

1. **Fork**: open the target repository page on GitHub (for example `open-vela/packages_apps`) and click **Fork** at the top right. You get a copy under your own account.
2. **Develop in your workspace**: after you fetch the code with `repo` as described in the [Development Guide](./hk_university_track_dev_guide.md), `packages_apps` is in `packages/apps` in your workspace, `packages_demos` is in `packages/demos`, and `vendor_allwinnertech` is in `vendor/allwinnertech`. Go into the matching directory and create a new branch:

   ```bash
   cd packages/apps
   git checkout -b my-app
   ```

3. **Add your app**: read the directory structure in the repository README and put your app in the directory closest to your app type. If you are not sure where it goes, say so in the PR and the reviewer will decide. Besides the C source, a native app needs four files: `Kconfig`, `Make.defs`, `CMakeLists.txt`, and `Makefile`. Follow the existing examples in the repository, or the hello_r528 example in the [Development Board Guide](./mibox_x1_board_guide.md).
4. **Commit to your local branch**:

   ```bash
   git add <your app directory>
   git commit -s -m "<one sentence describing this commit>"
   ```

   `-s` adds a `Signed-off-by` line to the commit message.
5. **Push to your fork**:

   ```bash
   git remote add myfork git@github.com:<your GitHub username>/packages_apps.git
   git push myfork my-app
   ```

6. **Open the PR**: open your fork on GitHub and click **Compare & pull request**. Check that the target repository is `open-vela/packages_apps` and the target branch is `dev-ai-contest-2026`, fill in the description, and create the PR.
7. **Follow the review**: watch for review comments and reply promptly. To make changes, keep committing and pushing to the same branch. The PR updates automatically.

## IV. What to Write in the PR

We suggest the PR description states:

- The name of your project, and one or two sentences about what it does.
- How to run it. For a Quick App, state which emulator configuration it runs on. For a native app, state which configuration to use, how to build it, and which command to type at `nsh>` to start it.
- Which development board peripherals it uses. Leave this out if you did not use the board.

## V. Checklist Before You Submit

- Every new file has a license header.
- The code follows the [openvela Code Style Check Guide](../contribute/code_style_check_guide.md).
- The PR contains only your project, with no unrelated formatting changes.
- No personal information, keys, or API keys are committed.
- You have signed the CLA for your first submission.

For the full contribution process, see [Contributing to openvela](../../CONTRIBUTING.md).
