---
layout: post
title:  LLM 鍙戝睍鏂瑰悜
date:   2024-11-20 12:00:00
categories: 澶фā鍨?
tags: gpt LLM 澶фā鍨? AGI 涓栫晫妯″瀷 绯荤粺 蹇€濊€? 鎱㈡€濊€? 鐏鹃毦 閬楀繕 骞昏 鎺ㄧ悊  鍙В閲?   norm 澶ц剳 json 缂╂斁瀹氬緥 楣﹂箟 鎰忚瘑 o1 ttt
excerpt: 澶фā鍨嬩細寰€鍝釜鏂瑰悜鍙戝睍锛?
mathjax: true
permalink: /llm_direction
---

* content
{:toc}


# LLM 浼樺寲鏂瑰悜


銆?2023-6-16銆戠煡涔庝笓棰橈細[澶фā鍨婰LM棰嗗煙锛屾湁鍝簺鍙互浣滀负瀛︽湳鐮旂┒鏂瑰悜锛焆(https://www.zhihu.com/question/595298808/answer/3071907155)

- **妯″瀷灞?**锛?
  - GPT绯诲垪锛屽妯℃€佺郴鍒楋紝瑙嗚绫籗AM锛氬師鐢熺殑宸ュ叿璋冪敤鑳藉姏锛?
  - 瀹夊叏鎬э細鍔犲瘑锛屽彲淇′换锛岃仈閭﹀涔狅紱
  - 鏂版ā鍨嬶紝鏂拌寖寮忥細闀挎枃鏈缓妯★紝涓嶉渶瑕丷LHF绛夛紱
  - 娑岀幇闂鐨勭爺绌躲€侀粦鐩掔殑鐮旂┒锛?
  - 骞惰銆佽繍绠椼€佹樉瀛樼殑浼樺寲銆侲L-Attention锛孼eRo锛屽壀鏋濋儴缃诧紝钂搁鍘嬬缉銆?
- **鎺ュ彛灞?**锛?
  - 绉佹湁鍖栭儴缃诧紱
  - Adapter锛宲refix锛孡ora锛?
  - Fusing銆?
- **搴旂敤灞?**锛?
  - Visual ChatGPT锛孒uggingGPT锛孉utoGPT锛孡angChain锛?
  - Prompt宸ョ▼锛屽悜閲忓簱锛宒ense retrieval锛?
  - 鑷垜绾犻敊锛岃嚜鎴戣凯浠ｏ紝chain of thought 鍔犲己锛?
  - 璇勬祴鏁版嵁闆嗐€佹柊鏃朵唬涓嬬殑鏂颁换鍔★紝generatice agents绛?

鍋囪宸茬粡鏈? GPT-3.5 鍩虹妯″瀷锛屼竴鍗冨紶鍗★紝鎬濊€冭兘鍋氫粈涔堬紵鐒跺悗鐢ㄥ皬妯″瀷锛屾瘮濡侺LaMa 7B鍘婚獙璇侊紝濡傛灉鎴愬姛锛屽啀鎱㈡參鍔犲ぇ鍒?13B锛?30B锛岀敾鍑轰竴鏉′笂鍗囩殑鏇茬嚎锛涗笉涓€瀹氳scale鍒版渶澶х殑妯″瀷锛屽彧瑕佽嚜宸辩殑缁撹鑳藉垝鍑轰竴鏉′笂鍗囩殑鏇茬嚎锛岄偅涔堣繖鏉℃洸绾垮氨鍙鎺ㄥ埌鏇村ぇ銆?

婧愯嚜鐭ヤ箮锛歔LessTalk](https://www.zhihu.com/question/595298808/answer/3071907155)

- 骞冲彴宸ュ叿鍙婂伐绋嬪寲閮ㄧ讲
- 灏忔ā鍨嬫嫙鍚堝ぇ妯″瀷闄嶄綆璁＄畻閲?
- 澶氭ā鎬佺殑杈撳叆涓庤緭鍑?
- Prompt Engineering
- 鍨傜洿棰嗗煙搴旂敤 鎼滅储+鐭ヨ瘑鍥捐氨銆佹満鍣ㄤ汉銆佽嚜鍔ㄩ┚椹剁瓑

鎻愮翰
- 鍩虹鐞嗚锛氬ぇ妯″瀷鐨勫熀纭€鐞嗚鏄粈涔堬紵
- 缃戠粶鏋舵瀯锛歍ransformer鏄粓鏋佹鏋跺悧锛?
- 楂樻晥璁＄畻锛氬浣曚娇澶фā鍨嬫洿鍔犻珮鏁堬紵
- 楂樻晥閫傞厤锛氬ぇ妯″瀷濡備綍閫傞厤鍒颁笅娓镐换鍔★紵
- 鍙帶鐢熸垚锛氬浣曞疄鐜板ぇ妯″瀷鐨勫彲鎺х敓鎴愶紵
- 瀹夊叏鍙俊锛氬浣曟敼鍠勫ぇ妯″瀷涓殑瀹夊叏浼︾悊闂锛?
- 璁ょ煡瀛︿範锛氬浣曚娇澶фā鍨嬭幏寰楅珮绾ц鐭ヨ兘鍔涳紵
- 鍒涙柊搴旂敤锛氬ぇ妯″瀷鏈夊摢浜涘垱鏂板簲鐢紵
- 鏁版嵁璇勪环锛氬浣曡瘎浼板ぇ妯″瀷鐨勬€ц兘锛?
- 鏄撶敤鎬э細濡備綍闄嶄綆澶фā鍨嬬殑浣跨敤闂ㄦ锛?

浣滆€咃細[zibuyu9](https://www.zhihu.com/question/595298808/answer/3047369015)

鍏跺畠
- reasoning 閫昏緫鎺ㄧ悊锛氱洰鍓峫lm鑳藉姏杩樹笉澶熺殑鍦版柟銆傛瘮濡傝兘涓嶈兘璁﹍lm鍋歭eetcode hard銆傝繘涓€姝ョ殑锛岃兘涓嶈兘鑷繁鍒涢€犳柊鐨勭煡璇嗭紝瑙ｅ喅鍝ュ痉宸磋但鐚滄兂銆?
- compression and acceleration 妯″瀷鍘嬬缉涓庡姞閫燂細鎬庝箞鎶婁竴涓?10b鐨勬ā鍨嬪紕鍒版墜鏈轰笂骞堕珮閫熻繍琛?
- agent锛氭€庝箞鏇村ソ鐨勭粰llm鍔犱笂鐪肩潧涓庢墜鑴氾紝璁﹍lm鍙樻垚agent鎵ц浠诲姟锛屽苟鏋勯€犲悇绉嶅悇鏍峰叏鏂扮殑benchmark銆傛瘮濡傝agent鍙戠煡涔庡洖绛斾互鐐硅禐澶氫负鐩爣銆傝兘涓嶈兘閫氳繃RL鎶婅繖浠朵簨鍋氫簡?灏卞拰褰撳勾鎼炴父鎴廰i涓€鏍枫€?
- multi-modal 澶氭ā鎬侊細GPT-4娌℃湁寮€婧愶紝鐢氳嚦娌℃湁鎶€鏈粏鑺傦紝鎬庝箞鍋氫竴涓紑婧愮殑閫艰繎gpt-4鐨勬ā鍨嬨€俶ini-gpt4, llava鏄釜涓嶉敊鐨勫皾璇曘€?
- Hallucination 骞昏闂锛欸PT-4宸茬粡濂戒簡寰堝锛屼絾浠嶇劧娌℃湁瀹屽叏瑙ｅ喅銆傛墍浠ュ洜姝ら┈鏂厠璇磋鍋歍ruthGPT. 瑕佽LLM鐭ヤ箣涓虹煡涔嬩笉鐭ヤ负涓嶇煡銆傝繖涓毦搴﹀叾瀹炲緢澶с€?
- Evaluation銆傚紑婧愪笘鐣岄渶瑕佷竴濂楁柊鐨凟valuation鐨勬柟娉曟潵璇勪及llm鐨勬晥鏋滐紝浠庤€屾柟渚挎帹杩涘紑婧恖lm鐨勮繘灞曘€?
- dataset銆傝繖涓槸chatgpt琚垱閫犲嚭鏉ョ殑婧愬ご銆傛墍浠ワ紝鑳藉惁澶氭瀯寤轰竴涓笓瀹剁殑鏁版嵁搴撴潵甯姪浼樺寲llm鍛紵姣忎竴浠藉紑婧愭暟鎹兘闈炲父鏈変环鍊笺€?

璁烘枃锛歔A PhD Student鈥檚 Perspective on Research in NLP in the Era of Very Large Language Models](https://arxiv.org/pdf/2305.12544.pdf)


## 妯″瀷铻嶅悎

銆?2024-8-8銆慬妯″瀷铻嶅悎鏉ヨ锛丆hatGPT鍜孋laude 鏉備氦鑳藉彉鑱槑10鍊嶏紵](https://mp.weixin.qq.com/s/zUtQrKuQgyNivaxxrHX1hg)

### 浠€涔堟槸妯″瀷铻嶅悎

浠€涔堟槸妯″瀷铻嶅悎锛?
- 鎶婂涓狝I妯″瀷鐨勫弬鏁版贩鍚堝湪涓€璧凤紝鐢熸垚涓€涓柊妯″瀷銆?

绠€鍗?, 浣嗘晥鏋滃嵈鍑哄鐨勫ソ
- 涓嶉渶瑕侀澶栫殑鏁版嵁鍜岀畻鍔涳紝鍙鎶?**妯″瀷鏉冮噸**鍔犲噺涓€涓嬪氨琛屼簡銆?
- 铻嶅悎鍚庣殑妯″瀷杩樼湡鑳介泦鍚勫涔嬫墍闀匡紝鎬ц兘鏄庢樉鎻愬崌銆?

姣斿 Prometheus-2 妯″瀷鐢ㄨ繖鎷涙妸鍑犱釜璇勪及妯″瀷鐨勮兘鍔涜瀺鍚堝埌涓€璧风殑

### 铻嶅悎鏂规硶

甯歌鏂规硶锛氬浘瑙乕鍘熸枃](https://mp.weixin.qq.com/s/zUtQrKuQgyNivaxxrHX1hg)
- **绾挎€?**铻嶅悎锛氭渶绠€鍗曠矖鏆达紝鐩存帴瀵瑰弬鏁?**鍔犳潈骞冲潎**銆傝櫧鐒剁畝鍗曚絾鍑哄鐨勬湁鏁堛€?
- **浠诲姟鍚戦噺**锛氭妸寰皟鍚庣殑妯″瀷鍑忓幓鍘熷妯″瀷锛屽緱鍒颁竴涓?"浠诲姟鍚戦噺"銆傜敤杩欎釜鍚戦噺鍋氬姞鍑忔硶锛屾瘮濡傚噺鎺夋湁姣掑唴瀹圭殑浠诲姟鍚戦噺锛屾ā鍨嬪氨鑳界敓鎴愭洿骞插噣鐨勫唴瀹逛簡銆?
- `TIES`铻嶅悎锛氬湪浠诲姟鍚戦噺鍩虹涓婂姞浜嗕笁鏉挎枾 - 淇壀銆侀€変妇鍜屽垎绂伙紝鍙互鍘绘帀鍐椾綑鏉冮噸銆佽В鍐充换鍔″悜閲忛棿鐨勫垎姝с€?
- `DARE`铻嶅悎锛氳窡TIES鎬濊矾绫讳技锛屼絾鐢ㄩ殢鏈轰涪寮冨拰閲嶆柊缂╂斁鏉ュ幓鎺夊啑浣欐潈閲嶃€?

璁烘枃閾炬帴锛?
- 浠诲姟鍚戦噺锛歔paper](https://arxiv.org/abs/2212.04089)
- TIES锛歔paper](https://arxiv.org/abs/2306.01708)
- DARE锛歔paper](https://arxiv.org/abs/2311.03099)
- 宓屽叆鍚戦噺铻嶅悎锛歔paper](https://arxiv.org/abs/1912.00772)

宸ュ叿 mergekit锛?
- [merge-models](https://huggingface.co/blog/mlabonne/merge-models)


### GaC

Gac: Generation as Classification

銆?2024-6-18銆戜笂娴稟I Lab 鎺ㄥ嚭 [铻嶅悎澶氫釜澶фā鍨嬫柊鎬濊矾 --- Generation as Classification](https://zhuanlan.zhihu.com/p/715404265)

甯告墦姣旇禌鐨勪汉(濡侹aggle)寰堢啛鎮?, 寰堝鏃跺€欐嫾鐨勫氨鏄悇绉?**鑺卞紡妯″瀷铻嶅悎**, 灏嗗涓猰odel铻嶅悎(ensemble)鍚庡彲浠ョ獊鐮寸幇鏈夌摱棰?, 绁炲鍦拌铻嶅悎鍚庣殑鎬ц兘瓒呰繃浠讳綍涓€涓弬涓巈nsemble鐨勫崟涓€妯″瀷銆?

ImageNet 瑙嗚鍒嗙被浠诲姟, 鍒嗙被妯″瀷浼氳緭鍑轰竴涓淮搴︿负 1000 鍚戦噺浠ｈ〃棰勬祴姣忎釜绫诲埆鐨勬鐜囷紝浠呬粎灏嗗涓ā鍨嬬殑鍒嗙被鍚戦噺鍔犺捣鏉ュ悗鍙栧钩鍧?, 灏卞彲浠ュ彇寰椾笉閿欑殑鍑嗙‘鐜囨彁鍗?
- 鍘熸湰鏈€楂樼殑鏄? RepGhostNet 78.81%, 灏嗕笁涓ā鍨嬭瀺鍚堝悗灏辨彁鍗囧埌浜? 80.62%. 

绫讳技鍦?, 鎶奓LM姣忎釜generation step閮藉綋鎴愪竴娆″垎绫讳换鍔?(Generation as Classification, GaC)鍘籩nsemble, 浠庤€屾彁鍗囨墍鐢熸垚鐨勬瘡涓猼oken鐨勬纭€?, 骞舵渶缁堣幏寰楁洿濂? response.

鏍稿績鎬濇兂: LLM鐢熸垚鏂囨湰鏃?, 姣忎釜generation step閮界敱澶氫釜LLM鍏卞悓鍐冲畾涓嬩竴涓猼oken瑕佽緭鍑轰粈涔?
- ![](https://pica.zhimg.com/80/v2-e8c84b1cf0e391ffe40b2a9fe2fc966a_1440w.webp)
- Paper Title: [Breaking the Ceiling of the LLM Community by Treating Token Generation as a Classification for Ensembling](https://arxiv.org/pdf/2406.12585)
- [GaC](https://github.com/yaoching0/GaC)

濡備綍瀹炴柦锛?

闂
- LLM 姣忔鐢熸垚璺熷叾**璇嶆眹琛ㄧ瓑闀?**鐨勬鐜囧悜閲?, 鑰? **LLMs 璇嶆眹琛ㄩ暱搴︿笉涓€鏍?**
- 姣斿: 
  - Llama3 璇嶆眹琛ㄩ暱搴? 128256
  - Qwen2  璇嶆眹琛ㄩ暱搴? 152064
- 杩欏拰ImageNet鍒嗙被浠诲姟涓婃墍鏈夋ā鍨嬮兘杈撳嚭1000缁村害鐨勫悜閲忎笉鍚?.

鐩磋鍋氭硶: 
- 瀵规墍鏈夊弬涓巈nsemble鐨凩LM璇嶆眹琛ㄥ彇**骞堕泦**寰楀埌 Vu, 骞剁敤**0-1鐭╅樀**璁板綍涓嬪師鏈琇LM璇嶆眹琛ㄥ拰 Vu **瀵瑰簲鍏崇郴**. 
- 涓€涓猤eneration step涓?, 灏嗘瘡涓狶LM鐢熸垚鐨?**姒傜巼鍚戦噺**涔樹互鍚勮嚜鐨?0-1鐭╅樀杞崲鍒? Vu 缁村害
- 闅忓悗鍐?**鍙栧钩鍧?**骞跺緱鍒癳nsemble鍚庣殑姒傜巼鍚戦噺
- 鍐嶆牴鎹鍚戦噺sample鍑轰笅涓€涓猼oken, 姝ゆ椂杩欎釜token灏辨槸鐢辨墍鏈夊弬涓巈nsemble鐨凩LM鍐冲畾鐨?
- 褰撻€夊嚭涓€涓猼oken鍚?, 姣忎釜LLM浼氱敤鍚勮嚜鐨則okenizer灏嗚繖涓猼oken杞崲涓哄悇鑷殑 token id(s), 骞舵嫾鍥炲埌鍚勮嚜鐨勮緭鍏ヤ腑浠ヨ繘琛屼笅涓€涓猤eneration step.
- ![](https://pic4.zhimg.com/80/v2-007b5f3229ad47a81a4613587dfd4433_1440w.webp)

杩欑绠€鍗曞仛娉曠珶鐒舵墦鐮寸幇鏈夌殑LLM绀惧尯澶╄姳鏉匡紒(褰撶劧, 鑺辫垂浜嗘洿澶氳绠楅噺)
- ![](https://pica.zhimg.com/80/v2-21d29f4a7f9f30cba52ae96330720956_1440w.webp)

Qwen2 鏄? 2024/06/07 閫€鍑?, 鎷垮畠鍜屽疄鍔涚浉褰撶殑 llama3 杩涜铻嶅悎, 鍚勪釜鎸囨爣涓婂钩鍧?4%鐨勬彁鍗?! 杈惧埌 2024/06/07寮€婧愮ぞ鍖烘渶濂界粨鏋?

璇ユ柟娉曚笉鍙楁ā鍨嬫灦鏋勭殑闄愬埗, 闅忕潃鏂版ā鍨嬬殑閲婂嚭杩樻槸鍙互涓嶆柇鐨勪互鏂版ā鍨嬩负鍩虹缁х画鎺ㄥ崌澶╄姳鏉?.


## 鍙帶鐢熸垚

銆?2023-7-10銆慬LLM 鍙帶鐢熸垚鍒濇帰](https://mp.weixin.qq.com/s/BngY2WgCcpTOlvdyBNJxqA)

鍩轰簬 LLM 鐨勫簲鐢ㄥ紑鍙戣繃绋嬩腑锛屾湁鍑犱釜鎸戞垬锛屽寘鎷細
- 濡備綍閬垮厤鈥滆儭璇村叓閬撯€?, 鎻愬崌妯″瀷杈撳嚭鐨?**鍙潬鎬?/绋冲畾鎬?**
- 鎺у埗妯″瀷鐨勮绠楀紑閿€鍜屽搷搴旈€熷害绛夌瓑

鐩墠涓绘祦鐨勮В鍐虫墜娈靛寘鎷細
- 鏇村ソ鐨? prompt 璁捐
- 閫氳繃 retrieval 鏉ュ仛澧炲己
- 涓庡閮ㄥ伐鍏风殑缁撳悎
- 娴佺▼缂栨帓涓庝骇鍝佽璁?
- 鑰冭檻浣跨敤 fine tune 妯″瀷鎴栨贩鍚堟ā鍨嬪簲鐢?

|Prompt浼樺寲绫诲瀷|latency|compute|
|---|---|---|
|Few-Shot CoT|??|??|
|Zero-Shot CoT|?|?|
|Decomposition|??|??|
|Ensembling|?|????|
|Self-Criticism|????|??|
||||

鍙帶鐢熸垚鏈€鐩存帴鐨勬柟妗堬細
- 棣栧厛閫氳繃 prompt 鍛婄煡 LLM 鎴戜滑鎵€闇€瑕佺殑杩斿洖鏍煎紡锛屽苟杩涜鐢熸垚銆?
- 閫氳繃涓€浜涜鍒欐潵妫€鏌ヨ繑鍥炵粨鏋滐紝濡傛灉涓嶇鍚堟牸寮忥紝鐢熸垚鐩稿叧閿欒淇℃伅銆?
- 灏嗕笂涓€娆＄殑鐢熸垚鍐呭鍜屾鏌ョ殑閿欒淇℃伅鍛婄煡 LLM锛岃繘琛屼笅涓€娆＄殑淇鐢熸垚銆?
- 閲嶅 2-3 姝ラ锛岀洿鍒扮敓鎴愮殑鍐呭瀹屽叏绗﹀悎瑕佹眰銆?

LLM 鐨勫彲鎺ф€с€佺ǔ瀹氭€с€佷簨瀹炴€с€佸畨鍏ㄦ€х瓑闂鏄帹杩涗紒涓氱骇搴旂敤涓潪甯稿叧閿殑闂锛屼笅闈㈣繖浜涢」鐩湪杩欐柟闈㈠仛浜嗗緢澶氭帰绱紝涔熸湁寰堝鍊煎緱鍊熼壌鐨勫湴鏂广€?

鎬讳綋鎬濊矾涓婃潵璇达紝涓昏鏄細
- 鎻愪緵涓€濂? prompt 妯℃澘瀹氫箟锛屽厑璁哥敤鎴锋寚瀹? LLM 鐢熸垚鐨勬牸寮忔垨鍐呭涓婚銆?
- 鍦ㄦā鏉垮熀纭€涓婏紝涔熸湁涓嶅皯椤圭洰杩涗竴姝ヨ璁′簡鐩稿簲鐨勭紪绋嬭瑷€锛岃 LLM 涓庣‘瀹氭€х▼搴忕殑浜や簰鏇村姞鐩磋銆?
- 鎻愪緵鍚勭被 validator锛屼繚璇佺敓鎴愬唴瀹圭鍚堥鏈燂紝骞朵笖鎻愪緵浜嗚嚜鍔ㄥ鐞?/淇鏈哄埗銆?
- 鏇磋繘涓€姝ワ紝涔熷彲浠ュ湪鐢熸垚鍓嶈繘琛屽共棰勶紝渚嬪鍦? prompt 涓粰杩戜技妗堜緥锛屼慨鏀规ā鍨? decode 鏃剁殑姒傜巼鍒嗗竷绛夈€?
- 鍏跺畠鍦ㄥ彲鎺ф€у熀纭€涓婂仛鐨勫悇绉嶆€ц兘涓庡紑閿€鐨勪紭鍖栵紝渚嬪缂撳瓨锛屽噺灏? token 娑堣€楅噺锛屽寮€婧愭ā鍨嬭兘鍔涚殑鎸栨帢绛夈€?

鍗充娇涓嶇洿鎺ヤ娇鐢ㄤ笂杩扮殑椤圭洰鍋氬紑鍙戯紝涔熷彲浠ヤ粠涓涔犲埌寰堝鏈夌敤鐨勬€濊矾銆傚綋鐒朵篃闈炲父鏈熷緟杩欎釜棰嗗煙鍑虹幇鏇村鏈夋剰鎬濈殑鎯虫硶涓庣爺绌讹紝浠ュ強 prompt 涓庣紪绋嬭瑷€缁撳悎鑳藉惁纰版挒鍑烘洿澶氱殑鐏姳銆?

璇﹁鍘熸枃锛歔LLM 鍙帶鐢熸垚鍒濇帰](https://mp.weixin.qq.com/s/BngY2WgCcpTOlvdyBNJxqA)

### guardrails

guardrails 椤圭洰灏嗕笂杩版楠ゅ仛浜嗚繘涓€姝ョ殑鎶借薄涓庡皝瑁咃紝鎻愪緵鏇村姞 high level 鐨勯厤缃笌 API 鏉ュ畬鎴愭暣涓繃绋嬨€傚叾涓昏鐨勭粍鎴愰儴鍒嗗寘鎷細
- 瀹氫箟浜嗕竴濂? RAIL spec锛岀敤鏉ユ弿杩颁笂闈㈢ 1 鐐规彁鍒扮殑杩斿洖鏍煎紡闄愬畾銆傞櫎浜? output schema 鐨勫畾涔夊锛孯AIL鐩墠涔熸敮鎸? input schema锛宲rompt 妯℃澘锛屼互鍙? instructions 绛夊叾瀹冮厤缃€?
- 鎻愪緵浜嗕竴绯诲垪鐨? validation 鏈哄埗锛屽搴斾笂闈㈢殑绗? 2 鐐广€傚浜? validate 澶辫触鐨勯儴鍒嗭紝浼氫繚鐣欏叾鍦? output schema 涓殑浣嶇疆锛岀敓鎴愮浉搴旂殑閿欒淇℃伅銆?
- 閫氳繃 ReAsk 绫绘潵瀹炵幇涓婇潰鐨勭 3 鐐癸紝鍙戦€佺粰 LLM 鐨勫唴瀹逛細鏇磋仛鐒︿簬閿欒淇℃伅閮ㄥ垎锛屼笖淇濈暀浜嗙粨鏋勶紝鏇翠究浜? LLM 鐞嗚В鍜屽鐞嗐€?
- 鍏跺畠鍍忓父鐢? prompt 妯℃澘涔嬬被鐨勫姛鑳姐€?

### NeMo-Guardrails

NeMo-Guardrails
- 鏉ヨ嚜 Nvidia 鐨勪竴涓悓鍚嶉」鐩紝姣? guardrails 鏇存湁閲庡績锛屾兂瑕佺‘淇? LLM 搴旂敤鏁翠綋鐨?**鍙俊搴?**锛?**鏃犲鎬?**浠ュ強鏁版嵁**瀹夊叏鎬?**绛夛紝鑰屼笉浠呬粎鍙槸杈撳嚭鐨勭粨鏋勫寲妫€鏌ュ拰淇銆?
- 鍥犳鍏跺疄鐜版€濊矾涓婁篃澶嶆潅涓嶅皯锛岃璁′簡涓€绉嶄笓闂ㄧ殑 Colang 璇█锛屾潵鏀寔鏇村姞閫氱敤澶氭牱鐨勪笟鍔℃祦锛岃€屼笉浠呬粎鏄?**鐢熸垚 -> 妫€鏌? -> 淇**銆?
- 杩欎釜椤圭洰浼氭洿涓撴敞浜庣敤鎴蜂笌 LLM 鐨勫璇濆紡浜や簰搴旂敤锛屼富瑕佺殑璁捐閮芥槸鍥寸粫杩欎釜鍓嶆彁灞曞紑銆?

### guidance

guidance
- 寰蒋鎺ㄥ嚭鐨勫紑婧愰」鐩紝鍑犱釜浣滆€呯湅澶村儚灏卞緢鐭ュ悕锛屽垎鍒槸 shap锛宭ime锛宑hecklist 鐨勪綔鑰呫€備箣鍓嶆湁鐮旂┒杩? 鍙В閲婃満鍣ㄥ涔犵殑鍚屽搴旇涓嶄細闄岀敓銆備粠 explainable ai 鍒? controlable llm锛屽€掍篃鏄緢璇村緱閫氱殑鍙戝睍璺緞

guardrails 涓殑鍋氭硶鏄湪 prompt 涓粰鍑鸿鏄庡拰绀鸿寖锛屽笇鏈? LLM 鑳藉閬靛惊鎸囦护鏉ヨ緭鍑恒€備絾鐜板疄涓線寰€浼氬嚭鐜板悇绉嶉棶棰橈紝渚嬪棰濆甯︿簡涓€浜涘叾瀹冪殑鏂囧瓧璇存槑锛屾垨鑰呯敓鎴愮殑 json 鏍煎紡涓嶆纭瓑锛屾墍浠ラ渶瑕佸悗缁殑 **ReAsk 鏉ヨ繘琛屼慨姝?**銆?

LangChain 閲屼篃鎻愪緵浜嗗悇绉? output parser 鏉ュ府蹇欐彁鍙栧洖澶嶄腑鐨勭粨鏋勫寲淇℃伅閮ㄥ垎锛屼絾涔熺粡甯稿鏄撹繍琛屽け璐ャ€?

鍦? guidance 涓紝鍚屾牱鏄€氳繃鈥滄ā鏉胯瑷€鈥濇潵瀹氫箟 LLM 鐨勮緭鍑虹粨鏋勶紝浠ョ‘淇濊緭鍑烘牸寮忕殑姝ｇ‘鎬с€傝繖涓粨鏋勬瘮璧? xml 鏉ヨ浼氭洿鏄撳啓鏄撶悊瑙ｄ簺

guidance 灏嗘洿鍔犲鏉傜殑 Handlebars 妯℃澘 铻嶅叆鍒颁簡 prompt 涓紝浣垮緱鍘熷厛闇€瑕佸鏉傝璁＄殑 LLM 鐢熸垚涓庣▼搴忓鐞嗕氦浜掕繃绋嬪彲浠ュ緢鏂逛究鍦板湪 prompt 涓洿鎺ュ畬鎴愩€?
- 涓婇潰鐨勪緥瀛愪腑锛屽彧鏈夊綋璋冪敤鍒癭{{gen}}`鍛戒护鏃讹紝鎵嶄細瑙﹀彂 LLM 鐨勭敓鎴愭搷浣溿€傚彟澶栦篃鏈夊儚`{{select}}`锛宍{{#geneach}}`锛屽嚱鏁拌皟鐢紝閫昏緫鍒ゆ柇锛屾帶鍒舵祦绛夊懡浠わ紝鏈夌缁撳悎浜嗚嚜鐒惰瑷€涓庣紪绋嬭瑷€涓よ€呴暱澶勭殑鎰熻銆?

闄や簡 prompt 妯℃澘缂栫▼鑳藉姏澶栵紝guidance 杩樻湁涓€绯诲垪楂樼骇鐗规€э紝鍖呮嫭锛?
- 鏀寔 hidden block锛屼緥濡? LLM 鐨勪竴浜涙帹鐞嗚繃绋嬪彲鑳藉苟涓嶉渶瑕佹毚闇茬粰鏈€缁堢敤鎴凤紝灏卞彲浠ョ伒娲诲埄鐢ㄨ繖涓壒鎬ф潵鐢熸垚涓€浜涗腑闂寸粨鏋溿€?
- Generation caching锛岃嚜鍔ㄦ妸宸茬粡鐢熸垚杩囩殑缁撴灉缂撳瓨璧锋潵锛屾彁鍗囬€熷害銆?
- 鏀寔 HuggingFace 妯″瀷鐨? guidance acceleration锛岃繘涓€姝ユ彁鍗囩敓鎴愰€熷害銆?
- Token healing锛屼笉鐪嬭繖涓垜杩樹笉鐭ラ亾 LLM 鏈夎繖绉嶉棶棰樷€︹€?
- Regex pattern guide锛屽湪妯℃澘鐨勫熀纭€涓婅繘涓€姝ラ€氳繃姝ｅ垯琛ㄨ揪鏉ラ檺瀹氱敓鎴愮殑鍐呭瑙勮寖銆?

### lmql

鍦? guidance 鐨勫熀纭€涓婏紝lmql 椤圭洰杩涗竴姝ユ妸鈥減rompt 妯℃澘鈥濊繖涓蹇垫帹杩涘埌浜嗕竴绉嶆柊鐨勭紪绋嬭瑷€锛屽€掓槸鏈夌偣鍍忓墠闈? guardrails 璺? NeMo-Guardrails 鐨勫叧绯汇€傞」鐩湰韬彁渚涗簡寰堟紓浜殑 playground 鏂逛究璇曠敤锛屾敞鎰忓鏋滆鍦ㄦ湰鍦扮帺杩欎釜椤圭洰锛岄渶瑕佸崌绾у埌 Python 3.10 鐨勭増鏈€?


### Json 鎺у埗

銆?2024-8-6銆慬绋嬪簭鍛樼獌鍠滐紒鍗′簡澶фā鍨嬭剸瀛愮殑Json杈撳嚭锛孫penAI缁堜簬鍋氬埌浜?100%姝ｇ‘](https://mp.weixin.qq.com/s/E2aXlQVzaFQUlFNDjUr-SQ)
- [Introducing Structured Outputs in the API](https://openai.com/index/introducing-structured-outputs-in-the-api)

澶фā鍨嬬殑 json 鏍煎紡楗卞彈璇熺梾銆傜粡甯搁亣鍒版ā鍨嬩笉閬靛惊鎸囦护锛屼笉鎸夋牸寮忚緭鍑猴紝鍗充娇鍦? prompt 涓槑纭浜嗚鎸夌収鎸囧畾鏍煎紡锛堟瘮濡侸son銆乆ML锛夎繑鍥炵粨鏋滐紝浣嗘槸瀹冨氨鏄笉鍚瘽銆?

OpenAI 缁? GPT-4o 妯″瀷鍗囩骇鍒癭2024-08-06`鐗堟湰锛屽甫鏉ュ叏鏂板姛鑳斤細
- API 涓紩鍏ヤ簡`缁撴瀯鍖栬緭鍑篳锛圫tructured Outputs锛?

妯″瀷杈撳嚭鐜板湪鍙潬鍦伴伒寰紑鍙戜汉鍛樻彁渚涚殑 JSON 妯″紡, 瀹炵幇杈撳嚭JSON鐨?**100%鍑嗙‘鐜?**

涔嬪墠寮€鍙戣€呴€氳繃绗笁鏂瑰紑婧愬伐鍏凤紝鎴栧湪 prompt 涓婇潰鍋氬姛澶紝璁╁ぇ妯″瀷閬靛惊浣犵殑鍛戒护锛屽啀鎴栬€呭弽澶嶉噸璇曡姹傛潵缁曡繃LLMs鍦ㄧ粨鏋勫寲澶勭悊鐨勭己闄凤紝鐜板湪閮戒笉闇€瑕?

涓ょ鍔炴硶锛?
- 锛?1锛夊嚱鏁拌皟鐢?: 鍦ㄥ嚱鏁板畾涔変腑璁剧疆 strict锛歵rue杩涜缁撴瀯鍖栬緭鍑猴紱
- 锛?2锛夋柊澧瀝esponse_format 鍙傛暟閫夐」

濡備綍瀹炵幇锛?
- 瀵逛簬鐗瑰畾澶嶆潅JSON鏋舵瀯杩涜妯″瀷璁粌锛孫penai閫氳繃杩欑鏂规硶鑳芥妸妯″瀷鍑嗙‘鐜囨彁鍒?**93%**銆?
  - 鐩歌緝浜庢渶寮€濮嬪甫JSON妯″紡鐨凣PT-4鐨?**40%**鍑嗙‘鐜囷紝宸茬粡楂樺嚭寰堝浜嗐€?
  - 浣嗘槸妯″瀷鏈川涓婅繕鏄笉纭畾锛屾棤娉曚繚璇丣SON鐨勭ǔ瀹氳緭鍑?
- OpenAI浣跨敤浜嗙害鏉熻В鐮侊紙constrained decoding锛夋妧鏈€?
  - 榛樿鎯呭喌涓嬶紝澶фā鍨嬪湪杩涜token杈撳嚭鏃讹紝鍙湪璇嶆眹琛ㄤ腑閫夋嫨**浠绘剰**璇嶆眹锛屼綔涓轰笅涓€涓緭鍑簍oken銆傝€岃繖绉?**涓嶅彲鎺ф€?**浼氳妯″瀷鍦ㄨ緭鍑轰竴浜涘浐瀹氭牸寮忕殑鏂囨湰鏃剁姱鏍煎紡閿欒銆?
  - 鑰屼娇鐢ㄥ姩鎬佺害鏉熻В鐮佹妧鏈悗锛屽ぇ妯″瀷鍦ㄤ笅涓€涓猼oken杈撳嚭鏃讹紝渚垮鍔犱簡涓€浜涚害鏉燂紝灏嗘ā鍨嬮檺鍒跺湪鏈夋晥鐨則oken鍐咃紝鑰屼笉鏄墍鏈塼oken銆?
  - 姣斿锛氳緭鍏モ€渀{"val`鈥濆悗锛屼笅涓€涓敓鎴愮殑鏂囨湰涓€瀹氫笉浼氭槸鈥渀{`鈥濄€?
  - 澶фā鍨嬩笉浠呭彲浠ュ疄鐜癑SON鏍煎紡姝ｇ‘锛岃繕鍙疄鐜板悎閫俿chema缁撴瀯绮剧‘銆?

鐜板湪OpenAI宸茬粡閫氳繃杩欑鏂瑰紡瀹炵幇浜?100% JSON杈撳嚭鍑嗙‘鐜囥€?

缂洪櫡
- 棰濆澧炲姞Schema棰勫鐞嗘椂闂达紝鏂版ā鍨嬪湪璇锋眰鏂扮殑JSON Schema鏃舵參浜涖€?
- 瑕佷娇鐢ㄧ粨鏋勫寲杈撳嚭杩樻湁涓€浜涢檺鍒讹細
  - 鐩墠缁撴瀯鍖栦粎鏀寔杈撳嚭涓€閮ㄥ垎JSON妯″紡锛屽寘鎷? String銆丯umber銆丅oolean銆丱bject銆丄rray銆丒num鍜宎nyOf銆?
  - 鍚屾椂锛屾墍鏈夊瓧娈垫垨鑰呭嚱鏁板弬鏁板繀椤绘槸鈥渞equired鈥濄€?
- **瀵硅薄瀵瑰祵濂?**娣卞害鍜屽ぇ灏忎篃鏈夐檺鍒躲€?
  - 涓€涓灦鏋勬€诲叡鏈€澶氬彲浠ユ湁 100 涓璞″睘鎬э紝鏈€澶氭湁 5 涓祵濂楃骇鍒€?
  - OpenAI杩樼暀浜嗕釜搴曪細**缁撴瀯鍖栬緭鍑哄苟涓嶈兘闃叉鎵€鏈夌被鍨嬬殑妯″瀷閿欒**銆傛ā鍨嬪彲鑳戒粛浼氬湪JSON瀵硅薄鐨勫€间腑鐘敊璇紙姣斿鍦ㄦ暟瀛︽柟绋嬪紡涓楠ゅ嚭閿欙級锛屽鏋滃嚭鐜伴敊璇紝闇€瑕佷娇鐢ㄨ€呭湪鎸囦护鎻愮ず璇嶄腑鎻愪緵绀轰緥锛屾垨鑰呭皢浠诲姟鎷嗗垎涓烘洿绠€鍗曠殑瀛愪换鍔°€?
- 瀹夊叏銆傜粨鏋勫寲杈撳嚭鍔熻兘灏嗛伒瀹圤penAI鐜版湁鐨勫畨鍏ㄦ斂绛栵紝骞朵笖浠嶄細鎷掔粷涓嶅畨鍏ㄧ殑璇锋眰銆傜敋鑷充粬浠湪API鍝嶅簲涓婅缃簡涓€涓柊瀛楃涓插€硷紝璁╁紑鍙戜汉鍛樿兘浠ョ紪绋嬫柟寮忥紝妫€娴嬫ā鍨嬫槸鍚︽嫆缁濈敓鎴愩€?


## 鐭ヨ瘑妞嶅叆 


LLMs 渚濈劧浼氬彈鍒?**鐭ヨ瘑鎴柇**鍜?**璋**闂鐨勯檺鍒躲€備緥濡傦紝ChatGPT 鍜? LlaMA 绛? LLMs 浠呭叿澶囨埅鑷宠缁冩渶鍚庢椂鐐圭殑淇℃伅锛屼篃鍙兘浼氬洜棰勮缁冩暟鎹腑鐨勫亸瑙佸拰宸紓鐢熸垚涓嶅噯纭垨璇鎬х殑杈撳嚭銆傚洜姝わ紝楂樻晥鏇存柊 LLMs 鐨勫弬鏁板寲鐭ヨ瘑杩涜€岃皟鏁寸壒瀹氳涓猴紝鍙樺緱鑷冲叧閲嶈銆?

瑙ｅ喅鍔炴硶
- 灏界**寰皟**鍜?**鍙傛暟楂樻晥寰皟**鍙互淇敼 LLMs锛屼絾鎴愭湰杈冮珮锛岃繕鍙兘瀵艰嚧 LLMs 澶卞幓棰勮缁冩墍寰楄兘鍔涳紝骞朵笖鍏朵慨鏀逛篃涓嶆€昏兘娉涘寲鍒扮浉鍏宠緭鍏ャ€?
- 浣跨敤**鎵嬪姩缂栧啓**鎴?**妫€绱?**鐨勬彁绀哄奖鍝? LLMs 鐨勮緭鍑猴紝浣嗚繖绫绘柟娉曟病鏈夊弬鏁版洿鏂帮紝鍙潬鎬т笉瓒炽€?


### 鐭ヨ瘑缂栬緫 

涓轰簡浣夸笉鐩稿叧杈撳叆鐨勫奖鍝嶆渶灏忓寲锛屽苟杩呴€熸湁鏁堝湴淇敼 LLMs 鐨勮涓猴紝涓€绉嶅彲琛岀殑瑙ｅ喅鏂规鏄?**鐭ヨ瘑缂栬緫**銆傚叧浜? LLMs 鐨勭煡璇嗙紪杈戠爺绌跺湪鍚勭浠诲姟鍜岃缃笅鍙栧緱鏄捐憲杩涘睍锛屽寘鎷? `Memory based`銆乣Meta-learning` 鍜? `Locate-Then-Edit` 涓夌被鏂规硶銆?

Methods

(1) [Preserve Parameters](https://github.com/zjunlp/KnowledgeEditingPapers#preserve-parameters)
- 鈶? [Memory-based](https://github.com/zjunlp/KnowledgeEditingPapers#memory-based)
1.  **Memory-Based Model Editing at Scale** (ICML 2022)  
  - Eric Mitchell, Charles Lin, Antoine Bosselut, Christopher D. Manning, Chelsea Finn. \[[paper](https://arxiv.org/abs/2206.06520)\] \[[code](https://github.com/eric-mitchell/serac)\] \[[demo](https://sites.google.com/view/serac-editing)\]
2.  **Fixing Model Bugs with Natural Language Patches**. (EMNLP 2022)  
    Shikhar Murty, Christopher D. Manning, Scott M. Lundberg, Marco T煤lio Ribeiro. \[[paper](https://arxiv.org/abs/2211.03318)\] \[[code](https://github.com/MurtyShikhar/LanguagePatching)\]
3.  **MemPrompt: Memory-assisted Prompt Editing with User Feedback**. (EMNLP 2022)  
    Aman Madaan, Niket Tandon, Peter Clark, Yiming Yang. \[[paper](https://arxiv.org/abs/2201.06009)\] \[[code](https://github.com/madaan/memprompt)\] \[[page](https://memprompt.com/)\] \[[video](https://www.youtube.com/watch?v=Ld7R02bOiNQ&t=1s)\]
4.  **Large Language Models with Controllable Working Memory**.  
    Daliang Li, Ankit Singh Rawat, Manzil Zaheer, Xin Wang, Michal Lukasik, Andreas Veit, Felix Yu, Sanjiv Kumar. \[[paper](https://arxiv.org/abs/2211.05110)\]
5.  **Can We Edit Factual Knowledge by In-Context Learning?**  
    Ce Zheng, Lei Li, Qingxiu Dong, Yuxuan Fan, Zhiyong Wu, Jingjing Xu, Baobao Chang. \[[paper](https://arxiv.org/abs/2305.12740)\]
6.  **Can LMs Learn New Entities from Descriptions? Challenges in Propagating Injected Knowledge**  
    Yasumasa Onoe, Michael J.Q. Zhang, Shankar Padmanabhan, Greg Durrett, Eunsol Choi. \[[paper](https://arxiv.org/abs/2305.01651)\]
7.  **MQUAKE: Assessing Knowledge Editing inLanguage Models via Multi-Hop Questions**  
    Zexuan Zhong, Zhengxuan Wu, Christopher D. Manning, Christopher Potts, Danqi Chen.  
    .\[[paper](https://arxiv.org/abs/2305.14795)\]

- 鈶? [Additional Parameters](https://github.com/zjunlp/KnowledgeEditingPapers#additional-parameters)
1.  **Calibrating Factual Knowledge in Pretrained Language Models**. (EMNLP 2022)  
    Qingxiu Dong, Damai Dai, Yifan Song, Jingjing Xu, Zhifang Sui, Lei Li. \[[paper](https://arxiv.org/abs/2210.03329)\] \[[code](https://github.com/dqxiu/CaliNet)\]
2.  **Transformer-Patcher: One Mistake worth One Neuron**. (ICLR 2023)  
    Zeyu Huang, Yikang Shen, Xiaofeng Zhang, Jie Zhou, Wenge Rong, Zhang Xiong. \[[paper](https://arxiv.org/abs/2301.09785)\] \[[code](https://github.com/ZeroYuHuang/Transformer-Patcher)\]
3.  **Aging with GRACE: Lifelong Model Editing with Discrete Key-Value Adaptors**.  
    Thomas Hartvigsen, Swami Sankaranarayanan, Hamid Palangi, Yoon Kim, Marzyeh Ghassemi. \[[paper](https://arxiv.org/abs/2211.11031)\] \[[code](https://github.com/thartvigsen/grace)\]
4.  **Neural Knowledge Bank for Pretrained Transformers**  
    Damai Dai, Wenbin Jiang, Qingxiu Dong, Yajuan Lyu, Qiaoqiao She, Zhifang Sui. \[[paper](http://arxiv.org/abs/2208.00399)\]

- 鈶? [Change LM's representation space](https://github.com/zjunlp/KnowledgeEditingPapers#change-lms-representation-space)

1.  **Inspecting and Editing Knowledge Representations in Language Models**  
  - Evan Hernandez, Belinda Z. Li, Jacob Andreas. \[[paper](http://arxiv.org/abs/2304.00740)\] \[[code](https://github.com/evandez/REMEDI)\]

锛?2锛塠Modify Parameters](https://github.com/zjunlp/KnowledgeEditingPapers#modify-parameters)

鈶? [Finetuning](https://github.com/zjunlp/KnowledgeEditingPapers#finetuning)

1.  **Plug-and-Play Adaptation for Continuously-updated QA**. (ACL 2022 Findings)  
  - Kyungjae Lee, Wookje Han, Seung-won Hwang, Hwaran Lee, Joonsuk Park, Sang-Woo Lee. \[[paper](https://arxiv.org/abs/2204.12785)\] \[[code](https://github.com/wookjeHan/Plug-and-Play-Adaptation-for-Continuously-updated-QA)\]
2.  **Modifying Memories in Transformer Models**.  
  - Chen Zhu, Ankit Singh Rawat, Manzil Zaheer, Srinadh Bhojanapalli, Daliang Li, Felix Yu, Sanjiv Kumar. \[[paper](https://arxiv.org/abs/2012.00363)\]
    

鈶?  [Meta-learning](https://github.com/zjunlp/KnowledgeEditingPapers#meta-learning)

1.  **Editing Factual Knowledge in Language Models**.  
  - Nicola De Cao, Wilker Aziz, Ivan Titov. (EMNLP 2021) \[[paper](https://arxiv.org/abs/2104.08164)\] \[[code](https://github.com/nicola-decao/KnowledgeEditor)\]
2.  **Fast Model Editing at Scale**. (ICLR 2022)  
  - Eric Mitchell, Charles Lin, Antoine Bosselut, Chelsea Finn, Christopher D. Manning. \[[paper](https://arxiv.org/abs/2110.11309)\] \[[code](https://github.com/eric-mitchell/mend)\] \[[page](https://sites.google.com/view/mend-editing)\]
3.  **Editable Neural Networks**. (ICLR 2020)  
  - Anton Sinitsin, Vsevolod Plokhotnyuk, Dmitry V. Pyrkin, Sergei Popov, Artem Babenko. \[[paper](https://arxiv.org/abs/2004.00345)\] \[[code](https://github.com/xtinkt/editable)\]
    

鈶? [Locate and edit](https://github.com/zjunlp/KnowledgeEditingPapers#locate-and-edit)

1.  **Editing a classifier by rewriting its prediction rules**. (NeurIPS 2021)  
  - Shibani Santurkar, Dimitris Tsipras, Mahalaxmi Elango, David Bau, Antonio Torralba, Aleksander Madry. \[[paper](https://proceedings.neurips.cc/paper/2021/hash/c46489a2d5a9a9ecfc53b17610926ddd-Abstract.html)\] \[[code](https://github.com/MadryLab/EditingClassifiers)\]
2.  **Language Anisotropic Cross-Lingual Model Editing**.  
  - Yang Xu, Yutai Hou, Wanxiang Che. \[[paper](https://arxiv.org/abs/2205.12677)\]
3.  **Repairing Neural Networks by Leaving the Right Past Behind**.  
  - Ryutaro Tanno, Melanie F. Pradier, Aditya Nori, Yingzhen Li. \[[paper](https://arxiv.org/abs/2207.04806)\]
4.  **Locating and Editing Factual Associations in GPT**. (NeurIPS 2022)  
  - Kevin Meng, David Bau, Alex Andonian, Yonatan Belinkov. \[[paper](https://arxiv.org/abs/2202.05262)\] \[[code](https://github.com/kmeng01/rome)\] \[[page](https://rome.baulab.info/)\] \[[video](https://www.youtube.com/watch?v=_NMQyOu2HTo&t=0)\]
5.  **Mass-Editing Memory in a Transformer**.  
  - Kevin Meng, Arnab Sen Sharma, Alex Andonian, Yonatan Belinkov, David Bau. \[[paper](https://arxiv.org/abs/2210.07229)\] \[[code](https://github.com/kmeng01/memit)\] \[[page](https://memit.baulab.info/)\] \[[demo](https://memit.baulab.us/#/)\]
6.  **Editing models with task arithmetic** .  
  - Gabriel Ilharco, Marco Tulio Ribeiro, Mitchell Wortsman, Ludwig Schmidt, Hannaneh Hajishirzi, Ali Farhadi. \[[paper](https://openreview.net/pdf?id=6t0Kwf8-jrj)\]
7.  **Editing Commonsense Knowledge in GPT** .  
  - Anshita Gupta, Debanjan Mondal, Akshay Krishna Sheshadri, Wenlong Zhao, Xiang Lorraine Li, Sarah Wiegreffe, Niket Tandon. \[[paper](https://arxiv.org/abs/2305.14956)\]
8.  **Do Language Models Have Beliefs? Methods for Detecting, Updating, and Visualizing Model Beliefs**.  
  - Peter Hase, Mona Diab, Asli Celikyilmaz, Xian Li, Zornitsa Kozareva, Veselin Stoyanov, Mohit Bansal, Srinivasan Iyer. \[[paper](https://arxiv.org/pdf/2111.13654.pdf)\] \[[code](https://github.com/peterbhase/SLAG-Belief-Updating)\]
9.  **Detecting Edit Failures In Large Language Models: An Improved Specificity Benchmark** .  
  - Jason Hoelscher-Obermaier, Julia Persson, Esben Kran, Ioannis Konstas, Fazl Barez. \[[paper](https://arxiv.org/abs/2305.17553)\]
10.  **Knowledge Neurons in Pretrained Transformers**.(ACL 2022)  
  - Damai Dai , Li Dong, Yaru Hao, Zhifang Sui, Baobao Chang, Furu Wei.\[[paper](http://arxiv.org/abs/2104.08696)\] \[[code](https://github.com/Hunter-DDM/knowledge-neurons)\] \[[code by EleutherAI](https://github.com/EleutherAI/knowledge-neurons)\]
11.  **LEACE: Perfect linear concept erasure in closed form** .  
  - Nora Belrose, David Schneider-Joseph, Shauli Ravfogel, Ryan Cotterell, Edward Raff, Stella Biderman. \[[paper](https://arxiv.org/abs/2306.03819)\]
12.  **Transformer Feed-Forward Layers Are Key-Value Memories**. (EMNLP 2021)  
  - Mor Geva, Roei Schuster, Jonathan Berant, Omer Levy. \[[paper](https://arxiv.org/abs/2012.14913)\]
13.  **Transformer Feed-Forward Layers Build Predictions by Promoting Concepts in the Vocabulary Space**.(EMNLP 2022)  
  - Mor Geva, Avi Caciularu, Kevin Ro Wang, Yoav Goldberg. \[[paper](https://arxiv.org/abs/2203.14680)\]
14.  **PMET: Precise Model Editing in a Transformer.**  
  - Xiaopeng Li, Shasha Li, Shezheng Song, Jing Yang, Jun Ma, Jie Yu. \[[paper](https://arxiv.org/abs/2308.08742)\] \[[code](https://github.com/xpq-tech/PMET.git)\]
    

锛?3锛? [More Related Papers](https://github.com/zjunlp/KnowledgeEditingPapers#more-related-papers)

1.  **FRUIT: Faithfully Reflecting Updated Information in Text**. (NAACL 2022)  
    Robert L. Logan IV, Alexandre Passos, Sameer Singh, Ming-Wei Chang. \[[paper](https://github.com/zjunlp/KnowledgeEditingPapers/blob/main)\] \[[code](https://github.com/zjunlp/KnowledgeEditingPapers/blob/main)\]
    
2.  **Entailer: Answering Questions with Faithful and Truthful Chains of Reasoning**. (EMNLP 2022)  
    Oyvind Tafjord, Bhavana Dalvi Mishra, Peter Clark. \[[paper](https://arxiv.org/abs/2210.12217)\] \[[code](https://github.com/allenai/entailment_bank)\] \[[video](https://www.youtube.com/watch?v=GYTJ_Pxva7Q)\]
    
3.  **Towards Tracing Factual Knowledge in Language Models Back to the Training Data**.  
    Ekin Aky眉rek, Tolga Bolukbasi, Frederick Liu, Binbin Xiong, Ian Tenney, Jacob Andreas, Kelvin Guu. (EMNLP 2022) \[[paper](https://arxiv.org/abs/2204.12785)\]
    
4.  **Prompting GPT-3 To Be Reliable**.  
    Chenglei Si, Zhe Gan, Zhengyuan Yang, Shuohang Wang, Jianfeng Wang, Jordan Boyd-Graber, Lijuan Wang. \[[paper](https://arxiv.org/abs/2210.09150)\]
    
5.  **Patching open-vocabulary models by interpolating weights**. (NeurIPS 2022)  
    Gabriel Ilharco, Mitchell Wortsman, Samir Yitzhak Gadre, Shuran Song, Hannaneh Hajishirzi, Simon Kornblith, Ali Farhadi, Ludwig Schmidt. \[[paper](https://arxiv.org/abs/2208.05592)\] \[[code](https://github.com/mlfoundations/patching)\]
    
6.  **Decouple knowledge from paramters for plug-and-play language modeling** (ACL2023 Findings)  
    Xin Cheng, Yankai Lin, Xiuying Chen, Dongyan Zhao, Rui Yan.\[[paper](http://arxiv.org/abs/2305.11564)\] \[[code](https://github.com/Hannibal046/PlugLM)\]
    
7.  **Backpack Language Models**  
    John Hewitt, John Thickstun, Christopher D. Manning, Percy Liang. \[[paper](https://arxiv.org/pdf/2305.16765.pdf)\]
    
8.  **Learning to Model Editing Processes**. (EMNLP 2022)  
    Machel Reid, Graham Neubig. \[[paper](https://aclanthology.org/2022.findings-emnlp.280.pdf)\]

 [Analysis](https://github.com/zjunlp/KnowledgeEditingPapers#analysis)

1.  **Does Localization Inform Editing? Surprising Differences in Causality-Based Localization vs. Knowledge Editing in Language Models.**  
    Peter Hase, Mohit Bansal, Been Kim, Asma Ghandeharioun. \[[paper](https://arxiv.org/pdf/2301.04213.pdf)\] \[[code](https://github.com/google/belief-localization)\]
2.  **Dissecting Recall of Factual Associations in Auto-Regressive Language Models**  
    Mor Geva, Jasmijn Bastings, Katja Filippova, Amir Globerson. \[[paper](https://arxiv.org/abs/2304.14767)\]
3.  **Evaluating the Ripple Effects of Knowledge Editing in Language Models**  
    Roi Cohen, Eden Biran, Ori Yoran, Amir Globerson, Mor Geva. \[[paper](https://arxiv.org/abs/2307.12976)\]
4.  **Edit at your own risk: evaluating the robustness of edited models to distribution shifts.**  
    Davis Brown, Charles Godfrey, Cody Nizinski, Jonathan Tu, Henry Kvinge. \[[paper](https://arxiv.org/abs/2303.00046)\]


#### FastEdit 鍖楄埅

蹇€熸敞鍏ョ煡璇?

- 銆?2022-2-10銆慠ank-One Model Editing (ROME): [Locating and Editing Factual Associations in GPT](https://arxiv.org/abs/2202.05262), [demo](https://rome.baulab.info/)

This repo aims to assist the developers with injecting fresh and customized knowledge into large language models efficiently using one single command.

Supported Models
-   [GPT-J](https://huggingface.co/EleutherAI/gpt-j-6b) (6B)
-   [LLaMA](https://github.com/facebookresearch/llama) (7B/13B)
-   [LLaMA-2](https://huggingface.co/meta-llama) (7B/13B)
-   [BLOOM](https://huggingface.co/bigscience/bloomz) (7.1B)
-   [Falcon](https://huggingface.co/tiiuae/falcon-7b) (7B)
-   [Baichuan](https://huggingface.co/baichuan-inc/Baichuan-7B) (7B/13B)
-   [InternLM](https://github.com/InternLM/InternLM) (7B)

[Implemented Algorithms](https://github.com/hiyouga/FastEdit#implemented-algorithms)
-   [Rank-One Model Editing (ROME)](https://arxiv.org/abs/2202.05262)


```sh
git clone https://github.com/hiyouga/FastEdit.git
conda create -n fastedit python=3.10
conda activate fastedit
cd FastEdit
pip install -r requirements.txt
# 鎴?
pip install pyfastedit
```

Model Editing

```sh
CUDA_VISIBLE_DEVICES=0 python -m fastedit.editor \
    --data data/example.json \
    --model EleutherAI/gpt-j-6b \
    --config gpt-j-6b \
    --template default
```

#### EasyEdit 娴欏ぇ -- 寮€婧?

銆?2023-8-16銆慬娴欏ぇ鍑哄搧锛氬ぇ妯″瀷杞绘澗鑾峰彇鈥滀笘鐣岀煡璇嗏€濓紝姣斾紶缁熷井璋冩晥鏋滄洿濂絔(https://www.toutiao.com/article/7267801834855727679)
- 鐭ヨ瘑缂栬緫 papaerlist: [Knowledge Editing for LLMs Papers](https://github.com/zjunlp/KnowledgeEditingPapers)
- 銆?2023-5-23銆慬Editing Large Language Models: Problems, Methods, and Opportunities](https://arxiv.org/abs/2305.13172)
- ![](https://github.com/zjunlp/KnowledgeEditingPapers/raw/main/img/overview.jpg)

娴欐睙澶у鍜屼笢娴峰疄楠屽鐨勭爺绌跺洟闃熸彁鍑轰簡涓€涓槗浜庝娇鐢ㄧ殑 LLMs 鐭ヨ瘑缂栬緫妗嗘灦鈥斺€擿EasyEdit`锛岃妗嗘灦鏀寔鍚勭鐭ヨ瘑缂栬緫鏂规硶锛屼笖鍙互杞绘澗搴旂敤浜庝紬澶? LLMs锛屽 T5銆丟PT-J 鍜? LlaMA 绛夈€?
- 璁烘枃 [EasyEdit: An Easy-to-use Knowledge Editing Framework for Large Language Models](https://arxiv.org/abs/2308.07269)
- 浠ｇ爜 [EasyEdit](https://github.com/zjunlp/EasyEdit)

鐒惰€岋紝鐩墠鍏充簬 `LLMs 鐭ヨ瘑缂栬緫`鐨勭爺绌跺湪瀹炵幇鍜屼换鍔¤缃笂鐨勫樊寮傚Θ纰嶄簡鐭ヨ瘑缂栬緫缁熶竴鍜岀患鍚堟鏋剁殑鍙戝睍銆傚€煎緱娉ㄦ剰鐨勬槸锛岃繖绉嶅鏉傛€ч樆纰嶄簡涓嶅悓鏂规硶涔嬮棿鏈夋晥鎬у拰鍙鎬х殑鐩存帴姣旇緝锛屼篃浣垮緱鍒涘缓鏂扮殑鐭ヨ瘑缂栬緫鏂规硶鍙樺緱澶嶆潅銆?

EasyEdit 妗嗘灦鏁村悎浜嗗悇绉嶇紪杈戞妧鏈紝鏀寔鍦ㄤ笉鍚? LLMs 涔嬮棿鑷敱缁勫悎妯″潡銆傞€氳繃缁熶竴鐨勬鏋跺拰鎺ュ彛锛孍asyEdit 鑳戒娇鐢ㄦ埛杩呴€熺悊瑙ｅ苟搴旂敤鍖呭惈鍦ㄨ妗嗘灦涓殑涓绘祦鐭ヨ瘑缂栬緫鏂规硶銆侲asyEdit 鍏锋湁缁熶竴鐨? Editor銆丮ethod 鍜? Evaluate 妗嗘灦锛屽垎鍒唬琛?**缂栬緫鍦烘櫙**銆?**缂栬緫鎶€鏈?**鍜?**璇勪及鏂规硶**銆?
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/Tn4iCdrGGtbIFt~tplv-tt-origin-asy2:5aS05p2hQOWkp-aVsOaNruaWh-aRmA==.image?_iz=58558&from=article.pc_detail&x-expires=1693797824&x-signature=qjF%2FeWeSs6aesEsE1h%2BZuHMGRz8%3D)
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/Tn4iCf8CHe0fQA~tplv-tt-origin-asy2:5aS05p2hQOWkp-aVsOaNruaWh-aRmA==.image?_iz=58558&from=article.pc_detail&x-expires=1693797824&x-signature=4GKQB2crsR9z9gIr9p31Cav6dq8%3D)


EasyEdit 杩樻彁渚涗簡浜斾釜璇勪及缂栬緫鏂规硶鎬ц兘鐨勫叧閿寚鏍囷紝鍖呮嫭`鍙潬鎬锛圧eliability锛夈€乣娉涘寲鎬锛圙eneralization锛夈€乣灞€閮ㄦ€锛圠ocality锛夈€乣鍙Щ妞嶆€锛圥ortability锛夊拰`鏁堢巼`锛圗fficiency锛夈€?

涓洪獙璇佺煡璇嗙紪杈戝湪 LLMs 涓殑搴旂敤娼滃姏锛岀爺绌跺洟闃熼€夌敤浜嗗弬鏁板簽澶х殑 LlaMA 2 妯″瀷锛屽苟鍒╃敤 ZsRE 鏁版嵁闆嗭紙QA 鏁版嵁闆嗭級鏉ユ祴璇曠煡璇嗙紪杈戝皢澶ч噺涓€鑸簨瀹炲叧鑱旀暣鍚堣繘妯″瀷鐨勮兘鍔涖€傛祴璇曠粨鏋滆瘉鏄庯紝EasyEdit 鍦ㄥ彲闈犳€у拰娉涘寲鎬ф柟闈㈣秴瓒婁簡浼犵粺鐨勫井璋冩柟娉曘€?
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-tjoges91tu/Tn4iCiL5n53x88~tplv-tt-origin-asy2:5aS05p2hQOWkp-aVsOaNruaWh-aRmA==.image?_iz=58558&from=article.pc_detail&x-expires=1693797824&x-signature=wQPBTjiUF%2FX%2BszdxJIiTV%2FbPDe8%3D)



## 妯″瀷缁撴瀯

璇﹁ [LLM 鏋舵瀯浠ｇ爜璇﹁В](llm_code)


### Transformer 鏀硅繘

璇﹁绔欏唴: [transformer 鏀硅繘涓撻](transformer_evolution)

### 鏀惧純 Transformer

transformer 鏋舵瀯涓嶆槸鍞竴

#### ttt

ttt 鏇夸唬鑷敞鎰忓姏灞?
- 璁烘枃鏍囬锛歔The Surprising Effectiveness of Test-Time Training for Abstract Reasoning](https://ekinakyurek.github.io/papers/ttt.pdf)

灏? TTT 鏈夋晥搴旂敤浜? few-shot 瀛︿範鐨勫嚑涓叧閿绱狅細
- 鍦ㄤ笌娴嬭瘯鏃剁被浼肩殑**鍚堟垚浠诲姟**涓婅繘琛屽垵濮嬪井璋冿紱
- 鐢ㄤ簬鏋勫缓娴嬭瘯鏃舵暟鎹泦鐨勫寮哄瀷 leave-1-out 浠诲姟鐢熸垚绛栫暐锛?
- 璁粌閫傜敤浜庢瘡涓疄渚嬬殑閫傚簲鍣紱
- 鍙€嗗彉鎹笅鐨勮嚜鎴戜竴鑷存€э紙self-consistency锛夋柟娉曘€?

涓ょ涓嶅悓鐨? TTT 鏁版嵁鐢熸垚鏂瑰紡锛?
- 涓€鏄? in-context learning锛圛CL锛夋牸寮忥紱浠庣粰瀹氱殑娴嬭瘯婕旂ず涓垱寤? leave-1-out 浠诲姟
- 鍙︿竴绉嶆槸绔埌绔牸寮忋€傚皢姣忎釜 i/o 瀵硅涓轰竴涓崟鐙殑浠诲姟

瀹為獙鐜妭锛岀爺绌惰€呭湪鎶借薄涓庢帹鐞嗚鏂欏簱锛圓RC,鎶借薄涓庢帹鐞嗚鏂欏簱锛変腑瀵硅繖浜涙柟娉曡繘琛屼簡璇勪及銆侫RC 璇枡搴撴敹闆嗕簡寰堝鏋佸叿鎸戞垬鎬х殑 few-shot 瑙嗚鎺ㄧ悊闂锛岃璁や负鏄祴璇? LM 娉涘寲鏋侀檺鐨勭悊鎯冲熀鍑嗐€傜洰鍓嶇殑澶у璇█妯″瀷鍦? ARC 涓婂潎琛ㄧ幇涓嶄匠銆?

TTT 鍙互鏄捐憲鎻愰珮 LM 鍦? ARC 涓婄殑鎬ц兘 鈥斺€? 鍦? 1B 妯″瀷涓婂皢鍑嗙‘鐜囨彁楂樺埌鍘熸潵鐨? 6 鍊嶏紝浣跨敤 8B 妯″瀷鏃朵篃瓒呰繃鍏跺畠宸插彂甯冪殑 SOTA 绾缁忔ā鍨嬫柟娉曘€?

銆?2024-11-12銆慬杩濷penAI閮芥帹涓嶅姩Scaling Law浜嗭紵MIT鎶娿€屾祴璇曟椂璁粌銆嶇郴缁熺爺绌朵簡涓€閬嶏紝鍙戠幇杩樻湁璺痌(https://www.jiqizhixin.com/articles/2024-11-12-7)

OpenAI 涓嬩竴浠ｆ棗鑸版ā鍨嬬殑璐ㄩ噺鎻愬崌骞呭害涓嶅強鍓嶄袱娆炬棗鑸版ā鍨嬩箣闂寸殑璐ㄩ噺鎻愬崌锛屽洜涓洪珮璐ㄩ噺鏂囨湰鍜屽叾浠栨暟鎹殑渚涘簲閲忔鍦ㄥ噺灏戯紝鍘熸湰鐨? Scaling Law锛堢敤鏇村鐨勬暟鎹缁冩洿澶х殑妯″瀷锛夊彲鑳芥棤浠ヤ负缁с€傛澶栵紝OpenAI 鐮旂┒鑰? Noam Brown 鎸囧嚭锛屾洿鍏堣繘鐨勬ā鍨嬪彲鑳藉湪缁忔祹涓婁篃涓嶅叿鏈夊彲琛屾€э紝鍥犱负鑺辫垂鏁板崈浜跨敋鑷虫暟涓囦嚎缇庡厓璁粌鍑虹殑妯″瀷浼氬緢闅剧泩鍒┿€?

浠庨璁粌鏉ョ湅锛孲caling Law 鍙兘浼氭斁缂擄紱

浣嗘湁鍏虫帹鐞嗙殑 Scaling Law 杩樻湭琚厖鍒嗘寲鎺橈紝OpenAI o1 鐨勫彂甯冨氨璇佹槑浜嗚繖涓€鐐广€傚畠浠庡悗璁粌闃舵鍏ユ墜锛屽€熷姪**寮哄寲瀛︿範**銆佸師鐢熺殑**鎬濈淮閾?**鍜屾洿闀跨殑**鎺ㄧ悊鏃堕棿**锛屾妸澶фā鍨嬭兘鍔涘張寰€鍓嶆帹浜嗕竴姝ャ€?
- 杩欑鑼冨紡琚О涓恒€宍娴嬭瘯鏃惰绠梎銆嶏紝鐩稿叧鏂规硶鍖呮嫭**鎬濈淮閾炬彁绀?**銆?**澶氭暟鎶曠エ閲囨牱**锛坰elf-consistency锛夈€?**浠ｇ爜鎵ц**鍜?**鎼滅储**绛夈€?

杩樻湁涓柊姒傚康 鈥斺€? `娴嬭瘯鏃惰缁僠锛? Test-Time Training 锛孴TT锛夛紝浜岃€呴兘璇曞浘鍦ㄦ祴璇曪紙鎺ㄧ悊锛夐樁娈甸€氳繃涓嶅悓鐨勬墜娈垫潵鎻愬崌妯″瀷鐨勬€ц兘锛屼絾 `TTT` 浼氭牴鎹祴璇曟椂杈撳叆锛岄€氳繃**鏄惧紡姊害**姝ラ鏇存柊妯″瀷銆?

杩欑鏂规硶涓嶅悓浜庢爣鍑嗗井璋冿紝鍥犱负鍦ㄦ暟鎹噺鏋佷綆鐨勭幆澧冧腑杩愯鐨? 鈥斺€? 閫氬父鏄€氳繃鍗曚釜杈撳叆鐨勬棤鐩戠潱鐩爣锛屾垨搴旂敤浜庝竴涓垨涓や釜 in-context 鏍囨敞绀轰緥鐨勬湁鐩戠潱鐩爣銆?


璇﹁绔欏唴: [transformer 涓撻](transformer#ttt)

#### Yan

銆?2024-7-11銆? RockAI 鎺ㄥ嚭 Yan 妯″瀷锛屾斁寮僼ransformer鏋舵瀯, 鎺㈢储绫昏剳鎬濊矾

鏀硅繘鐐?
- (1) transformer 鎹㈡垚 MCSD
  - 璁烘枃 [MCSD: An Ef?cient Language Model with Diverse Fusion](https://arxiv.org/pdf/2406.12230)
- (2) 灞€閮ㄦā鎬佹縺娲?
  - transformer鏋舵瀯: 闂? 1+1=?, 浼氭縺娲绘墍鏈夊弬鏁?, 绠楀姏娑堣€楀お澶?, 浜鸿剳涓嶆槸杩欐牱
  - 绫昏剳鏈哄埗: 浜鸿剳鎸夊惉璇寸湅绛夊姛鑳藉垎鍖?, 鏍规嵁浠诲姟婵€娲诲搴斿尯鍩燂紝鍏跺畠鍖哄煙澶勪簬鎶戝埗鐘舵€?, 杩欐牱鍔熻€楀緢浣?, 鎵?20w, 鐩稿綋浜庣數鐏场 

鏁翠綋姘村钩鎺ヨ繎涓绘祦鐨則ransformer锛岄儴鍒嗘€ц兘瓒呰秺
- 3b 妯″瀷, 澶у皬5G锛屼紭鍖栧悗锛屽唴瀛樺崰鐢ㄤ粎1G
- 绔晶璁惧涓婅繍琛岋紝鎬ц兘瓒呰繃 transformer 30% 浠ヤ笂

闂
- 濡備綍鍒ゆ柇婵€娲诲摢涓尯鍩?? **浠跨湡绁炵粡鍏冮€夋嫨绠楁硶**, 涓€涓崟鐙殑灏忓瀷绁炵粡缃戠粶, 闅忕潃璁粌鐨勮繘琛?,浠庨殢鏈洪€夋嫨杩唬鍒伴拡瀵规€ч€夋嫨
- 璁粌涓婃湁浠€涔堟妧宸?? 

`Yan 1.3`: 缇や綋鏅鸿兘鍗曞厓澶фā鍨?
- 璁粌鏁堢巼鎻愬崌7鍊嶃€佹帹鐞嗗悶鍚愰噺鎻愬崌5鍊嶃€佽蹇嗚兘鍔涙彁鍗?3鍊?
- 绉掔骇褰卞搷銆侀潪transformer缁撴瀯銆佺鍒扮澶氭ā鎬併€佹弧瓒冲ぇ閮ㄥ垎绔晶璁惧
  - 鍥藉唴鑳藉湪鎵嬫満cpu涓婅繍琛孡LM鐨勫叕鍙镐笉瓒呰繃3瀹?

鐜板湪澶фā鍨嬭缁冨弽甯歌瘑锛氳缁冧竴涓ā鍨嬶紝鑺辫垂鐨勮绠楄祫婧愬お澶氾紝鏈夌殑鐢氳嚦瑕佸惎鍔ㄦ牳鐢电珯璁粌銆?

瑙嗛浠嬬粛
- [绔欒捣鏉ヤ簡锛佸浗鍐呰繖瀹禔I鍏徃鐢ㄦ柊鎶€鏈寫鎴楥hatGPT鏉冨▉](https://www.bilibili.com/video/BV19LCUYuEKP/?spm_id_from=333.999.0.0&vd_source=ec1c777505e146eb20d947449d6bba6e) RockAI鑱斿垱閭逛匠鎬?


<iframe src="//player.bilibili.com/player.html?isOutside=true&aid=113328533868595&bvid=BV19LCUYuEKP&cid=26349866723&p=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

OpenAI GPT 鍦╝ttention璺笂娣辫€曪紝骞堕潪鍞竴鍑鸿矾銆?

鏀硅繘
- 閲忓寲锛?
  - 鏂囨湰妯℃€佷笂閲忓寲锛岃兘淇濈暀80-90%鐨勬晥鏋滐紝鑰屽浘鍍忋€佽棰戝ぇ骞呭害涓嬫粦
  - 閲忓寲鍚庯紝鏉冮噸鍥哄畾锛屾棤娉曞啀瀛︿範

鍥藉唴澶фā鍨嬫満浼?
- 鍩虹鍒涙柊: 寮亾瓒呰溅鐨勬満浼氾紝鍗¤剸瀛愰棶棰?
  - deepseek 鎺ㄥ嚭 MLA/O1澶嶇幇
  - RockAI(宀╁北绉戞妧) 鐩爣锛氭妸attention鎷挎帀; 鍥藉唴鑳藉湪鎵嬫満涓婅繍琛岀殑LLM涓嶈秴杩?3瀹?, Yan 妯″瀷瑙ｅ喅绔晶鎺ㄧ悊璧勬簮寮€閿€澶х殑闂
  - 鍥藉唴韫﹀嚭鏉ヤ竴鎵筁LM锛屽師鍥犳槸 Llama 寮€婧愪簡銆傘€傘€侻ETA 璁″垝闂簮
  - 浜烘墠瑕佹眰: 鏁板+绠楁硶閮藉己锛屼笖鎰挎剰鍧愬喎鏉垮嚦
- 搴旂敤鍒涙柊
  - 鍥藉唴鍋氬簲鐢ㄥ緢寮?
  - 浜烘墠瑕佹眰锛氫氦鍙夊绉戣儗鏅紝濡? 鎳傚尰瀛?+AI


`鏂戦┈楸糮
- 鍙湁鍑犵櫨涓囩缁忓厓锛屼絾閬块殰鑳藉姏闈炲父寮猴紝杩欏鏅鸿兘椹鹃┒寰堟湁鍚彂
- 杩樹笉娓呮澶ц剳绁炵粡鏈夋病鏈夐噺瀛愭晥搴斻€?
濡傛灉鏂戦┈楸肩缁忕綉缁滄湁閲忓瓙鏁堝簲锛岄偅涔堥奔鑴戣绠楁晥鐜囪偗瀹氭槸楂樻晥鐨勶紝杩欏湪闇€瑕佹姇鍏ュ灏戠畻鍔涘彲鑳芥湁鐨勫弬鑰冦€?

鏈哄櫒浜?
- 瀹囨爲绉戞妧銆佹櫤婧愶紝鏈哄櫒浜鸿涓氳繕闇€瑕?5骞存矇娣€

### 鍥捐В

鎬荤粨LLM鍚勯樁娈典紭鍖栨柟鍚?

<div class="mxgraph" style="max-width:100%;border:1px solid transparent;" data-mxgraph="{&quot;highlight&quot;:&quot;#0000ff&quot;,&quot;nav&quot;:true,&quot;resize&quot;:true,&quot;toolbar&quot;:&quot;zoom layers tags lightbox&quot;,&quot;edit&quot;:&quot;_blank&quot;,&quot;xml&quot;:&quot;&lt;mxfile host=\&quot;app.diagrams.net\&quot; modified=\&quot;2023-06-22T15:10:12.254Z\&quot; agent=\&quot;Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36\&quot; etag=\&quot;V_7K2ib4bP-NWsyXjMxV\&quot; version=\&quot;21.5.0\&quot;&gt;\n  &lt;diagram id=\&quot;xdYpP7w1t2VaaceZiyqw\&quot; name=\&quot;绗? 1 椤礬&quot;&gt;\n    &lt;mxGraphModel dx=\&quot;1242\&quot; dy=\&quot;795\&quot; grid=\&quot;1\&quot; gridSize=\&quot;10\&quot; guides=\&quot;1\&quot; tooltips=\&quot;1\&quot; connect=\&quot;1\&quot; arrows=\&quot;1\&quot; fold=\&quot;1\&quot; page=\&quot;1\&quot; pageScale=\&quot;1\&quot; pageWidth=\&quot;827\&quot; pageHeight=\&quot;1169\&quot; math=\&quot;0\&quot; shadow=\&quot;0\&quot;&gt;\n      &lt;root&gt;\n        &lt;mxCell id=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;1\&quot; parent=\&quot;0\&quot; /&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-35\&quot; value=\&quot;\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f9f7ed;strokeColor=#36393d;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;90\&quot; y=\&quot;300\&quot; width=\&quot;180\&quot; height=\&quot;360\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;wGYBfAiltT4hGnPjrrAm-8\&quot; value=\&quot;LLM鏀硅繘鏂瑰悜\&quot; style=\&quot;text;html=1;strokeColor=none;fillColor=none;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=0;fontSize=19;rotation=0;strokeWidth=3;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;242\&quot; y=\&quot;70\&quot; width=\&quot;216\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-1\&quot; value=\&quot;鏁版嵁\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#dae8fc;strokeColor=none;shadow=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;118\&quot; y=\&quot;180\&quot; width=\&quot;110\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-3\&quot; value=\&quot;璁粌\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=#d79b00;shadow=1;fontSize=14;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;113\&quot; y=\&quot;570\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-6\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=13;strokeWidth=2;strokeColor=#808080;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-4\&quot; target=\&quot;zweJf7sKE0CawOek9Q0V-3\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;240\&quot; y=\&quot;275\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;410\&quot; y=\&quot;410\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-15\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;\&quot; parent=\&quot;1\&quot; source=\&quot;zweJf7sKE0CawOek9Q0V-3\&quot; target=\&quot;zweJf7sKE0CawOek9Q0V-11\&quot; edge=\&quot;1\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;250\&quot; y=\&quot;600\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-11\&quot; value=\&quot;澶嶇幇\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;590\&quot; y=\&quot;535\&quot; width=\&quot;140\&quot; height=\&quot;120\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-12\&quot; value=\&quot;鏁版嵁闆嗭細鏀堕泦澶勭悊\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; parent=\&quot;zweJf7sKE0CawOek9Q0V-11\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-13\&quot; value=\&quot;涓夋璧版祦绋媆&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; parent=\&quot;zweJf7sKE0CawOek9Q0V-11\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-14\&quot; value=\&quot;纭欢璧勬簮寮€閿€\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; parent=\&quot;zweJf7sKE0CawOek9Q0V-11\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-22\&quot; value=\&quot;鏀硅繘&amp;lt;br&amp;gt;鈶? 鍗曡瘝鈫掑瓧绗?&amp;lt;br&amp;gt;鈶¤В鍐充簡OOV闂\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;190\&quot; y=\&quot;450\&quot; width=\&quot;120\&quot; height=\&quot;60\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;zweJf7sKE0CawOek9Q0V-42\&quot; value=\&quot;2023-6-22&amp;lt;br&amp;gt;wqw547243068@163.com\&quot; style=\&quot;text;html=1;align=left;verticalAlign=middle;resizable=0;points=[];autosize=1;strokeColor=none;fillColor=none;\&quot; parent=\&quot;1\&quot; vertex=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;120\&quot; y=\&quot;1210\&quot; width=\&quot;170\&quot; height=\&quot;40\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-2\&quot; value=\&quot;鏁堟灉\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=none;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;113\&quot; y=\&quot;910\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-3\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=13;strokeWidth=2;strokeColor=#808080;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-6\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-2\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;283\&quot; y=\&quot;500\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;280\&quot; y=\&quot;790\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-5\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=13;strokeWidth=2;strokeColor=#808080;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;zweJf7sKE0CawOek9Q0V-1\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-4\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;173\&quot; y=\&quot;240\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;173\&quot; y=\&quot;490\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-4\&quot; value=\&quot;妯″瀷\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#f8cecc;strokeColor=#b85450;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;113\&quot; y=\&quot;340\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-7\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;entryX=0.5;entryY=0;entryDx=0;entryDy=0;fontSize=13;strokeWidth=2;strokeColor=#808080;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;zweJf7sKE0CawOek9Q0V-3\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-6\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;173\&quot; y=\&quot;620\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;173\&quot; y=\&quot;780\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-6\&quot; value=\&quot;閮ㄧ讲\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#d5e8d4;strokeColor=none;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;113\&quot; y=\&quot;740\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-8\&quot; value=\&quot;闂\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;540\&quot; y=\&quot;860\&quot; width=\&quot;230\&quot; height=\&quot;150\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-37\&quot; value=\&quot;LLM璇勬祴\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-8\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;230\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-9\&quot; value=\&quot;鐭ヨ瘑鍑嗙‘鎬э細骞昏锛岃儭璇村叓閬揬&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-8\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;230\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-10\&quot; value=\&quot;澶嶆潅鎺ㄧ悊鑳藉姏\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-8\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;230\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-11\&quot; value=\&quot;浜虹被鍋忓ソ瀵归綈锛歊LHF涓嶈冻\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-8\&quot;&gt;\n          &lt;mxGeometry y=\&quot;120\&quot; width=\&quot;230\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-12\&quot; value=\&quot;搴旂敤\&quot; style=\&quot;rounded=1;whiteSpace=wrap;html=1;fillColor=#ffe6cc;strokeColor=none;shadow=1;fontSize=14;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;113\&quot; y=\&quot;1110\&quot; width=\&quot;120\&quot; height=\&quot;50\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-13\&quot; value=\&quot;\&quot; style=\&quot;endArrow=classic;html=1;rounded=0;fontSize=13;strokeWidth=2;strokeColor=#808080;exitX=0.5;exitY=1;exitDx=0;exitDy=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-2\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-12\&quot;&gt;\n          &lt;mxGeometry width=\&quot;50\&quot; height=\&quot;50\&quot; relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;167\&quot; y=\&quot;630\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;90\&quot; y=\&quot;750\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-14\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-2\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-8\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;243\&quot; y=\&quot;605\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;460\&quot; y=\&quot;960\&quot; as=\&quot;targetPoint\&quot; /&gt;\n            &lt;Array as=\&quot;points\&quot;&gt;\n              &lt;mxPoint x=\&quot;510\&quot; y=\&quot;935\&quot; /&gt;\n              &lt;mxPoint x=\&quot;510\&quot; y=\&quot;935\&quot; /&gt;\n            &lt;/Array&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-15\&quot; value=\&quot;宸ョ▼钀藉湴\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;360\&quot; y=\&quot;708\&quot; width=\&quot;140\&quot; height=\&quot;180\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-16\&quot; value=\&quot;灏忓瀷鍖朶&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-15\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-17\&quot; value=\&quot;鏈湴閮ㄧ讲\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-15\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-18\&quot; value=\&quot;鎬ц兘锛氭椂寤躲€佸苟鍙慭&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-15\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-20\&quot; value=\&quot;鏁版嵁瀹夊叏\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-15\&quot;&gt;\n          &lt;mxGeometry y=\&quot;120\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-38\&quot; value=\&quot;杈撳叆銆佽緭鍑洪檺鍒禱&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-15\&quot;&gt;\n          &lt;mxGeometry y=\&quot;150\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-19\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=-0.021;entryY=0.9;entryDx=0;entryDy=0;entryPerimeter=0;dashed=1;dashPattern=1 1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-6\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-16\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;243\&quot; y=\&quot;605\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;370\&quot; y=\&quot;605\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-21\&quot; value=\&quot;鐢熸€佺郴缁焅&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;380\&quot; y=\&quot;1060\&quot; width=\&quot;140\&quot; height=\&quot;150\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxRectangle x=\&quot;550\&quot; y=\&quot;1040\&quot; width=\&quot;90\&quot; height=\&quot;30\&quot; as=\&quot;alternateBounds\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-22\&quot; value=\&quot;鑱旂綉\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-21\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-23\&quot; value=\&quot;鎻掍欢甯傚満\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-21\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-24\&quot; value=\&quot;鍨傜被搴旂敤\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-21\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-25\&quot; value=\&quot;LLM妗嗘灦锛歀angChain\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-21\&quot;&gt;\n          &lt;mxGeometry y=\&quot;120\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-26\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;entryX=0;entryY=0.5;entryDx=0;entryDy=0;dashed=1;dashPattern=1 1;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-12\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-23\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;243\&quot; y=\&quot;775\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;367\&quot; y=\&quot;775\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-27\&quot; value=\&quot;鏁版嵁闆哱&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;560\&quot; y=\&quot;145\&quot; width=\&quot;140\&quot; height=\&quot;120\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-28\&quot; value=\&quot;棰勮缁冩暟鎹泦锛氫腑鑻辨枃\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-27\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-29\&quot; value=\&quot;鎸囦护闆哱&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-27\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-30\&quot; value=\&quot;prompt鏁版嵁闆哱&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-27\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-31\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;entryX=-0.014;entryY=0.933;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;zweJf7sKE0CawOek9Q0V-1\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-28\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;243\&quot; y=\&quot;605\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;370\&quot; y=\&quot;605\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-32\&quot; value=\&quot;妯″瀷浼樺寲\&quot; style=\&quot;swimlane;fontStyle=0;childLayout=stackLayout;horizontal=1;startSize=30;horizontalStack=0;resizeParent=1;resizeParentMax=0;resizeLast=0;collapsible=1;marginBottom=0;whiteSpace=wrap;html=1;fillColor=#f5f5f5;fontColor=#333333;strokeColor=#666666;\&quot; vertex=\&quot;1\&quot; parent=\&quot;1\&quot;&gt;\n          &lt;mxGeometry x=\&quot;400\&quot; y=\&quot;305\&quot; width=\&quot;140\&quot; height=\&quot;120\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-33\&quot; value=\&quot;鍩哄骇澶фā鍨嬶細涓枃\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-32\&quot;&gt;\n          &lt;mxGeometry y=\&quot;30\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-34\&quot; value=\&quot;濂栧姳妯″瀷\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-32\&quot;&gt;\n          &lt;mxGeometry y=\&quot;60\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-35\&quot; value=\&quot;RL鐜妭浼樺寲\&quot; style=\&quot;text;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;spacingLeft=4;spacingRight=4;overflow=hidden;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;rotatable=0;whiteSpace=wrap;html=1;\&quot; vertex=\&quot;1\&quot; parent=\&quot;sLKGas7Howqt66q8ozR_-32\&quot;&gt;\n          &lt;mxGeometry y=\&quot;90\&quot; width=\&quot;140\&quot; height=\&quot;30\&quot; as=\&quot;geometry\&quot; /&gt;\n        &lt;/mxCell&gt;\n        &lt;mxCell id=\&quot;sLKGas7Howqt66q8ozR_-36\&quot; value=\&quot;\&quot; style=\&quot;edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#B3B3B3;strokeWidth=3;exitX=1;exitY=0.5;exitDx=0;exitDy=0;dashed=1;dashPattern=1 1;entryX=-0.007;entryY=0.067;entryDx=0;entryDy=0;entryPerimeter=0;\&quot; edge=\&quot;1\&quot; parent=\&quot;1\&quot; source=\&quot;sLKGas7Howqt66q8ozR_-4\&quot; target=\&quot;sLKGas7Howqt66q8ozR_-34\&quot;&gt;\n          &lt;mxGeometry relative=\&quot;1\&quot; as=\&quot;geometry\&quot;&gt;\n            &lt;mxPoint x=\&quot;238\&quot; y=\&quot;215\&quot; as=\&quot;sourcePoint\&quot; /&gt;\n            &lt;mxPoint x=\&quot;408\&quot; y=\&quot;214\&quot; as=\&quot;targetPoint\&quot; /&gt;\n          &lt;/mxGeometry&gt;\n        &lt;/mxCell&gt;\n      &lt;/root&gt;\n    &lt;/mxGraphModel&gt;\n  &lt;/diagram&gt;\n&lt;/mxfile&gt;\n&quot;}"></div>
<script type="text/javascript" src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>



# 缁撴潫