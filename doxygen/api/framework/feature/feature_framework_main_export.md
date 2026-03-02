# feature_framework_main_export API

为 Feature 框架管理者提供的一系列接口，用于创建 Feature 框架管理者以及设置管理者的属性。

## 快应用框架示例代码

```cpp
#ifdef CONFIG_FEATURE_FRAMEWORK
    FeatureManagerCreateInfo ft_info;
    ft_info.raw_ctx = (FeatureRawContextHandle)(qrt->env.ctx);
    ft_info.release_cb = nullptr;
    ft_info.manager_type = FEATURE_MANAGER_JS;
    ft_info.package_name = app->packageName();
    qrt->pFeatureMgr = FeatureCreateManager(&ft_info);
    FeatureSetArgsErrorCb(qrt->pFeatureMgr, on_feature_args_error, qrt);
    FeatureSetManagerUserData(qrt->pFeatureMgr, "app", app);
    FeatureSetUVLoop(qrt->pFeatureMgr, qrt->loop);
#endif
```

```eval_rst

.. doxygenfile:: feature_main_exports.h
  :project: doxygen

```
