# Media Focus API

Media Focus 即音频焦点（Audio Focus），用于协调多个音频流的播放优先级。在多音频流混合播放的场景中，音频焦点机制确保同一时间只有一个音频流作为主音频输出，其他音频流降为次要音频或暂停播放。

音频焦点采用合作抢占机制。未使用 Media Focus 的应用仍然可以播放音频，但无法接入音频焦点管理体系。此时可能出现非策略性的声音混合，影响用户体验。

## media_focus.h

```eval_rst

.. doxygenfile:: media_focus.h
  :project: doxygen
```
