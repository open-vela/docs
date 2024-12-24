# Contributing to openvela

\[ English | [简体中文](CONTRIBUTING_zh-cn.md) \]

openvela is developed by an active team of software engineers and researchers. You are welcome to join the openvela open source community and make any contribution to improve this project!

openvela mainly follows the Apache License 2.0 license, please refer to the LICENSE file for details.

## Sign the CLA

In order to participate in community contributions, you need to sign the corresponding Contributor License Agreement (CLA). Here are the specific steps for different platforms:

- **Gitee platform**:
  - Please visit the [Gitee CLA signing page](https://gitee.com/organizations/open-vela/cla/zs6b7c48u6juka2tsnrnkzx6k88np85e) to complete the signing.
  - You can check the signing status through [My CLA Status](https://gitee.com/profile/clas).

- **GitHub platform**:
  - After submitting a new Pull Request (PR), the system will prompt you to complete the CLA signing. Please follow the prompts to complete the signing process.

## Bug reports

If you think you have found a bug in openvela, first make sure you have tested with the latest version of openvela (your problem may already be fixed).

If not, search the issue list to see if there is already a similar problem.

## Feature requests

Please submit an issue describing the feature you would like to see added, why you need it, and how you expect it to work.

## Contributing code and documentation changes

If you want to add new features or fix some bugs to openvela, please check if there are similar issues. If not, please create a new issue to discuss your ideas with others.

### Branch strategy

- **trunk**: The **trunk** branch does not accept pull request
- **dev**: Fork the code from the **dev** branch and push a pull request

### Tips for code changes

- Following these tips prior to raising a pull request will speed up the review cycle.
- Add integration tests, if applicable
- Lines that are not part of your change should not be edited (e.g. don't format unchanged lines, don't reorder existing imports)
- Add the appropriate license headers to any new files

### Submitting your changes

1. Test your changes

    Run the test suite to make sure that nothing is broken.

2. Sign the Contributor License Agreement

    Please make sure you have signed our Contributor License Agreement. We are not asking you to assign copyright to us, but to give us the right to distribute your code without restriction. We ask this of all contributors in order to assure our users of the origin and continuing existence of the code. You only need to sign the CLA once.

3. **Rebase your changes**

    Update your local repository with the most recent code from the main openvela repository, and rebase your branch on top of the latest main branch. We prefer your initial changes to be squashed into a single commit. Later, if we ask you to make changes, add them as separate commits. This makes them easier to review. As a final step before merging we will either ask you to squash all commits yourself or we'll do it for you.

4. Submit a pull request

    Push your local changes to your forked copy of the repository and submit a pull request. In the pull request, choose a title which sums up the changes that you have made, and in the body provide more details about what your changes do. Also mention the number of the issue where discussion has taken place, eg "Closes #123".

### How to deal with conflicts

Normally, you don't need to rebase your pull request unless there is a merge conflict with the master branch. When GitHub prompts that your pull request "cannot be merged automatically", use the following command to rebase your pull request onto the latest master branch:

1. Rebase to the latest master branch

    ```Bash
    git remote add upstream https://github.com/open-vela/[repository].git
    git fetch upstream
    git rebase upstream/dev
    ```

2. Git may show some conflicts when it cannot merge, such as `conflict.cpp`, you need to manually modify the file to resolve the conflict and mark it as resolved after resolution

    ```Bash
    git add conflict.cpp
    ```

3. You can continue the rebase by the following ways

    ```Bash
    git rebase --continue
    ```

4. Push to your fork, and the pull request will be updated

    ```Bash
    git push --force
    ```