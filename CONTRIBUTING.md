# Contributing to openvela

\[ English | [简体中文](CONTRIBUTING_zh-cn.md) \]

openvela is developed by an active team of software engineers and researchers.You are welcome to join openvela, an open source community, and contribute in any way to this project!

openvela is mainly subject to Apache License 2.0. See the LICENSE file for details.

## Sign the CLA

In order to participate in community contributions, you need to sign a Contributor License Agreement before contributing to the community. Here are the specific steps for different platforms:

- **Gitee platform**:
  - Please visit the [Gitee CLA signing page](https://gitee.com/organizations/open-vela/cla/zs6b7c48u6juka2tsnrnkzx6k88np85e) to complete the signing.
  - You can check the signing status through [My CLA Status](https://gitee.com/profile/clas).

- **GitHub platform**:
  - After submitting a new Pull Request (PR), the system will prompt you to complete the CLA signing. Please follow the prompts to complete the signing process.

## Bug reports

If you think there is an error in openvela, make sure you have tested it with the latest version of openvela (the problem may have been fixed).

If not, search the issue list to see if there is already a similar problem.

## Feature request

Please submit an issue describing the feature you would like to add, why you need it, and how it is expected to work.

## Contributing code and documentation

If you want to add new features to openvela or fix some bugs, first check if similar issues already exist. If not, create a new issue and share your views.


### Branching strategy

- **trunk**: **trunk** branches do not accept pull requests
- **dev**: fork code from **dev** branch and push a pull request

### Tips Before Submitting Code

Follow these tips before making a pull request to speed up the review.

- Add appropriate unit tests
- Add integration tests if applicable
- Lines that are not part of your change should not be edited (e.g. don't format unchanged lines, don't reorder existing imports)
- Add the appropriate license headers to any new files

### Submitting your changes

1. Test your changes

    Run the test suite to make sure that nothing is wrong.
  
2. Sign the Contributor License Agreement

    Make sure you have signed our Contributor License Agreement (CLA). We are not asking you to assign copyright to us, but to give us the right to distribute your code without restriction. We ask all contributors to sign it in order to assure our users of the origin and continuing existence of the code. You only need to sign the CLA once.

3. **Rebase your changes**

    Update your local repository with the latest code from the main openvela repository, and rebase your branch on top of the latest main branch. We prefer your initial changes to be squashed into a single commit. Later, if we ask you to make changes, add them as separate commits. This makes them easier to review. As a final step before merging, we will either ask you to squash all commits yourself or we'll do it for you.

4. Submit a pull request

  Push your local changes to your forked copy of the repository and submit a pull request. In the pull request, choose a title which sums up the changes made. In the body text, provide details about the changes. Also mention the number of the issue; for example, “Closing #123".

### Resolving Conflicts

When the platform indicates that your pull request "can't automatically merge", use the following command to rebase the pull request on top of the latest main branch:

1. Rebase to the latest main branch

    ```Bash
    git remote add upstream https://github.com/open-vela/[repository].git
    git fetch upstream
    git rebase upstream/dev
    ```

2. Git may show conflicts when it can't merge, e.g. “conflict.cpp”. You need to modify the file manually to resolve the conflict, and mark it as resolved afterwards

    ```Bash
    git add conflict.cpp
    ```

3. Continue rebasing with:

    ```Bash
    git rebase --continue
    ```

4. Push to your fork, and the pull request will be updated

    ```Bash
    git push --force
    ```