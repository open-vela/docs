# Contributing to openvela

[ English | [简体中文](CONTRIBUTING_zh-cn.md)]

openvela is developed by an active team of software engineers and researchers.You are welcome to join openvela, an open source community, and contribute in any way to this project!

openvela is mainly subject to Apache License 2.0. See the LICENSE file for details.

## Signing the Contributor License Agreement (CLA)

In order to participate in community contributions, you need to sign a Contributor License Agreement before contributing to the community. Here are the specific steps for different platforms:

- **Gitee platform**:
    - Please visit the [Gitee CLA signing page](https://gitee.com/organizations/open-vela/cla/zs6b7c48u6juka2tsnrnkzx6k88np85e) to complete the signing.
    - You can check the signing status through [My CLA Status](https://gitee.com/profile/clas).

- **GitHub platform**:
    - After submitting a new Pull Request (PR), the system will prompt you to complete the CLA signing. Please follow the prompts to complete the signing process.

## Bug Reports

If you think there is an error in openvela, make sure you have tested it with the latest version of openvela (the problem may have been fixed).

If not, search the issue list to see if there is already a similar problem.

## Feature Requests

Please submit an issue describing the feature you would like to add, why you need it, and how it is expected to work.

## Code Submission

If you want to add new features to openvela or fix some bugs, first check if similar issues already exist. If not, create a new issue and share your views.

### Branching Strategy

- **trunk**: **trunk** branches do not accept pull requests
- **dev**: fork code from **dev** branch and push a pull request

### Tips Before Submitting Code

Follow these tips before making a pull request to speed up the review.

- Add appropriate unit tests.
- Add integration tests if applicable.
- Lines that are not part of your change should not be edited (e.g. **don't format unchanged lines, don't reorder existing imports**).
- Add the appropriate license headers to any new files.

### Before Submitting Your Code

Following these guidelines before creating a new pull request will help speed up the review and merge process.

- **Follow the Code Style Guide**: Ensure your code submission conforms to the [openvela Code Style Check Guide](./en/contribute/code_style_check_guide.md). Running local checks before submitting can help prevent unnecessary failures in the Continuous Integration (CI) pipeline.
- **Add License Headers**: Add the standard license header to all new files.
- **Add Unit Tests**: Include appropriate unit tests for your code changes to verify their correctness.
- **Add Integration Tests**: If your changes involve interactions between multiple modules, add corresponding integration tests.
- **Keep Commits Atomic**: Do not modify code unrelated to your changes. A single submission should focus on an independent feature or fix, avoiding unrelated formatting adjustments or code refactoring.

### Submitting Your Changes

1. Check current status.

    ```Bash
    # View working directory status
    git status
    ```

2. Stage changes.

    ```Bash
    # Add specific files to staging area
    git add path/to/changed/file.cpp
    # Or add all changes
    git add .
    ```

3. Commit changes.

    ```Bash
    # Create commit
    git commit -m "Concise commit message"
    # Or use detailed commit message
    git commit
    ```

4. Configure upstream repository.

    ```Bash
    # Display existing remote repository addresses
    git remote -v
    # Add upstream remote repository reference (only needed first time)
    git remote add upstream git@github.com:open-vela/[repository].git
    # Display existing remote repository addresses (should include origin and upstream)
    git remote -v
    ```

5. Fetch latest code and **rebase**.

    ```Bash
    # Fetch latest code from upstream repository
    git fetch upstream
    # Rebase current branch to latest main branch
    git rebase upstream/dev
    ```

6. Resolve conflicts (if any).

    ```Bash
    # Check conflict status (recommended)
    git status
    # Edit conflict files (e.g., conflict.cpp), using any editor like nano, vim, VSCode, etc.
    nano conflict.cpp
    # Mark as resolved
    git add conflict.cpp
    # Continue rebase operation after resolving all conflicts
    git rebase --continue
    # Confirm rebase completion status
    git status
    ```

7. Force push updates:

    ```Bash
    # Force push updated branch to your remote repository
    git push --force origin dev
    ```

#### 4 Create Pull Request

1. Visit your forked repository on GitHub.
2. Click the **New pull request** button.
3. Click **Create pull request** to create the pull request.
4. Fill in the pull request information.

#### 5 Follow-up Work After Pull Request

- Monitor the review comments on your pull request.
- Respond promptly to reviewer feedback.
- If modifications are needed, make changes on the same branch and push.