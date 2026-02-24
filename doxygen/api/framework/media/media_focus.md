# media focus API

Media Focus 又称为 Audio Focus/ Audio 焦点。目的是给多个音频流混合一起放送场场景提供播放策略，协助实现同一时间内只有一个音频作为主音频内容被放送，其他音频变为次要音频或暂停输出的使用场景。Media Focus 的机制为合作抢占型，不使用 media focus 应用依旧可以播放音乐，但无法接入到音频焦点管理体系，此时出现的非策略性声音混合可能会对用户使用体验造成影响。

## media_focus.h

```eval_rst

.. doxygenfile:: media_focus.h
  :project: doxygen
```
