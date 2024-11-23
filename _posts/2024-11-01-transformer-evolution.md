---
layout: post
title:  Transformer 鏀硅繘鏂规
date:   2024-11-01 16:52:00
categories: 娣卞害瀛︿範 
tags: 娣卞害瀛︿範 NLP Transformer BERT GPT Attention BeamSearch seq2seq 鏉ㄦ楹? XLNet 寰幆鏅鸿兘 roformer rwkv 鑻忓墤鏋? 妫€绱? 鑺墖 搴忓垪鍖? 娉ㄦ剰鍔? 涓夎摑涓€妫? 甯曠疮鎵? retnet yoco kan 閫氱敤閫艰繎瀹氱悊 鍙犲姞瀹氱悊 鏍锋潯 鍙鍖? ttt 涓夎摑涓€妫?
excerpt: Transformer 鏄ぇ妯″瀷鍞竴閫夋嫨涔堬紵
mathjax: true
permalink: /transformer_direction
---

* content
{:toc}


# Transformer 鏀硅繘鏂规

## Transformer 闂


銆?2023-9-18銆慬RetNet锛氫竾浼楁湡寰呯殑 Transformers 鏉€鎵媇(https://mp.weixin.qq.com/s/HhRtxONjzkoOmSRqixX50g), [澶存潯](https://www.toutiao.com/article/7304956621552501285/)

Transformer 宸叉垚涓哄ぇ璇█妯″瀷涓婄殑鏋舵瀯锛屽洜涓哄畠鏈夋晥鍦板厠鏈嶄簡寰幆绁炵粡缃戠粶 (RNN) 鐨勯『搴忚缁冮棶棰樸€?

鐒惰€岋紝Transformer 骞朵笉瀹岀編锛屽洜涓轰粎瑙ｅ喅浜嗘墍璋撯€渀impossible triangle`鈥濈殑**涓?**鏉¤噦銆?

鈥滀笉鍙兘涓夎鈥濅唬琛ㄥ綋鍓嶅簭鍒楁ā鍨嬫棤娉曞悓鏃跺疄鐜?**璁粌骞惰鎬?**銆?**浣庢垚鏈帹鐞?**浠ュ強**寮哄ぇ鎬ц兘**鐨勬墍鏈?3涓湡鏈涚淮搴︺€?
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-axegupay5k/e154053c06d24a3a8c24253b5185346e~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1701422819&x-signature=oxc1OeNc6B1%2BDAdIQ%2BaOw8jw%2BA0%3D)

涓夎涓婄殑鏂规硶琛ㄧず瀹炵幇鐨勪袱涓淮搴︼紝浣嗙己灏戠涓変釜椤剁偣鐨勬墍闇€灞炴€с€?
- ![](https://p3-sign.toutiaoimg.com/tos-cn-i-6w9my0ksvp/7c1f587ebec642bf9332284352e4a64d~noop.image?_iz=58558&from=article.pc_detail&lk3s=953192f4&x-expires=1701422819&x-signature=nYJb%2B%2FFDdkA1f%2F5FLtlAkG5XEVY%3D)


## 鍙В閲婃€?


### 鐧界洅 transformer -- CRATE

銆?2023-11-30銆慬銆孏PT-4鍙槸鍦ㄥ帇缂╂暟鎹€嶏紝椹瘏鍥㈤槦閫犲嚭鐧界洅Transformer锛屽彲瑙ｉ噴鐨勫ぇ妯″瀷瑕佹潵浜嗗悧锛焆(https://mp.weixin.qq.com/s/ErrCWbz8zDqSYkC9DH79Mg)

浼厠鍒╁拰棣欐腐澶у鐨刞椹瘏`鏁欐巿棰嗗鐨勪竴涓爺绌跺洟闃熺粰鍑轰簡鑷繁鐨勬渶鏂扮爺绌剁粨鏋滐細
> 鍖呮嫭 GPT-4 鍦ㄥ唴鐨勫綋鍓? AI 绯荤粺鎵€鍋氱殑姝ｆ槸鍘嬬缉銆?

鎻愬嚭鐨勬柊娣卞害缃戠粶鏋舵瀯 CRATE锛岄€氳繃鏁板鏂瑰紡楠岃瘉浜嗚繖涓€鐐广€?
- CRATE 鏄竴绉?**鐧界洅 Transformer**锛屽叾涓嶄粎鑳藉湪鍑犱箮鎵€鏈変换鍔′笂涓?**榛戠洅 Transformer** 鐩稿缇庯紝鑰屼笖杩樺叿澶囬潪甯稿嚭鑹茬殑**鍙В閲婃€?**銆?

鍩轰簬姝わ紝椹瘏鏁欐巿杩樺湪 Twitter 涓婂垎浜簡涓€涓湁瓒ｇ殑瑙佽В锛?
- 鏃㈢劧褰撳墠鐨? AI 鍙槸鍦ㄥ帇缂╂暟鎹紝閭ｄ箞灏卞彧鑳藉涔犲埌鏁版嵁涓殑**鐩稿叧鎬? / 鍒嗗竷**锛屾墍浠ュ氨骞朵笉鐪熸鍏峰**鍥犳灉鎴栭€昏緫鎺ㄧ悊**鎴栨娊璞℃€濊€冭兘鍔涖€?

鍥犳锛屽綋浠婄殑 AI 杩樼畻涓嶆槸 AGI锛屽嵆渚胯繎骞存潵鍦ㄥ鐞嗗拰寤烘ā澶ч噺楂樼淮鍜屽妯℃€佹暟鎹柟闈紝娣卞害瀛︿範鍦ㄥ疄楠屼腑鍙栧緱浜嗗法澶х殑鎴愬姛銆?

杩欑鎴愬姛褰掑姛浜庢繁搴︾綉缁滆兘鏈夋晥瀛︿範鏁版嵁鍒嗗竷涓?**鍙帇缂╃殑浣庣淮缁撴瀯**锛屽苟灏嗚鍒嗗竷杞崲涓虹畝绾︼紙鍗崇揣鍑戜笖缁撴瀯鍖栫殑锛夎〃寰併€傝繖鏍风殑琛ㄥ緛鍙敤浜庡府鍔╄澶氫笅娓镐换鍔★紝姣斿瑙嗚銆佸垎绫汇€佽瘑鍒拰鍒嗗壊銆佺敓鎴愩€?

琛ㄥ緛瀛︿範鏄€氳繃鍘嬬缉寮忕紪鐮佸拰瑙ｇ爜瀹炵幇鐨?

鐧界洅娣卞害缃戠粶鐞嗚銆備负瀛︿範绱у噾鍜岀粨鏋勫寲鐨勮〃寰佹彁鍑轰簡涓€涓粺涓€鐩爣锛屾湁鍘熺悊淇濊瘉鐨勪紭鑹害搴﹂噺銆傚浜庡涔犲埌鐨勮〃寰侊紝璇ョ洰鏍囨棬鍦ㄦ棦浼樺寲鍏跺湪缂栫爜鐜囦笅闄嶆柟闈㈢殑鍐呭湪澶嶆潅鎬э紝涔熶紭鍖栧叾鍦ㄧ█鐤忔€ф柟闈㈢殑澶栧湪澶嶆潅鎬с€傝鐩爣绉颁负 `绋€鐤忕巼涓嬮檷`锛坰parse rate reduction锛夈€?

涓轰簡浼樺寲杩欎釜鐩爣锛屾彁鍑哄涔犱竴涓?**澧為噺鏄犲皠搴忓垪**锛屾ā鎷熷睍寮€鐩爣鍑芥暟鐨勬煇浜涚被浼兼搴︿笅闄嶇殑杩唬浼樺寲鏂规銆傝繖寰楀埌涓€涓被浼? Transformer 鐨勬繁搴︾綉缁滄灦鏋勶紝骞朵笖瀹冨畬鍏ㄦ槸涓€涓€岀櫧鐩掋€嶁€斺€? 鍏朵紭鍖栫洰鏍囥€佺綉缁滅畻瀛愬拰瀛︿範鍒扮殑琛ㄥ緛鍦ㄦ暟瀛︿笂鏄畬鍏ㄥ彲瑙ｉ噴鐨勩€?

杩欎釜鐧界洅娣卞害鏋舵瀯鍛藉悕涓? `CRATE` 鎴? `CRATE-Transformer`锛岃繖鏄? `Coding-RATE transformer` 鐨勭缉鍐欍€傝繕閫氳繃鏁板鏂瑰紡璇佹槑杩欎簺澧為噺鏄犲皠鍦ㄥ垎甯冪殑鎰忎箟涓婃槸鍙€嗙殑锛屽苟涓斿畠浠殑閫嗘槧灏勬湰璐ㄤ笂鐢卞悓涓€绫绘暟瀛︾畻瀛愭瀯鎴愩€?

鍥犳锛屽彲浠ュ皢鍑犱箮瀹屽叏涓€鏍风殑 CRATE 鏋舵瀯鐢ㄤ簬缂栫爜鍣ㄣ€佽В鐮佸櫒鎴栬嚜鍔ㄧ紪鐮佸櫒銆?

## 妯″瀷缁撴瀯

濡傛灉璇? RetNet 鏄粠**骞宠鎺ㄧ悊鏁堣兘**鐨勮搴﹂潻鏂颁簡缃戠粶鏋舵瀯锛岄偅涔? BitNet 鍒欎粠姝ｄ氦瑙掑害鎻愬崌浜嗘帹鐞嗘晥鐜囥€?

杩欎袱鑰呯殑缁撳悎锛屼互鍙婅瀺鍚堝叾浠栨彁鍗囨ā鍨嬫晥鐜囩殑鎶€鏈瘮濡傛贩鍚堜笓瀹舵ā鍨嬶紙MoE锛夊拰绋€鐤忔敞鎰忓姏鏈哄埗锛圫parse Attention锛夛紝灏嗘垚涓烘湭鏉ュ熀纭€妯″瀷缃戠粶鏋舵瀯鐨勫熀纭€銆?


### RetNet

銆?2023-9-18銆慬RetNet锛氫竾浼楁湡寰呯殑 Transformers 鏉€鎵媇(https://mp.weixin.qq.com/s/HhRtxONjzkoOmSRqixX50g), [澶存潯](https://www.toutiao.com/article/7304956621552501285/)

寰蒋鐨? RetNet 浣嶄簬杩欎釜鈥渀impossible triangle`鈥濈殑姝ｄ腑蹇冿紝鑳滆繃浜嗘墍鏈夊皾璇曡繃浣嗘湭鑳藉疄鐜拌繖涓€澹妇鐨勬柟娉曘€俁etNet 璁炬硶鍦ㄥ崟涓鏋朵笅瀹炵幇鎵€鏈夊睘鎬с€?

绐佺牬锛?
- RetNet 鍏锋湁鏇村ソ鐨勮瑷€寤烘ā鎬ц兘
- RetNet 鍐呭瓨娑堣€楅檷浣庝簡 3.4 鍊?
- 鈥?.8.4 鍊嶆洿楂樼殑鍚炲悙閲?
- 鈥﹀欢杩熼檷浣? 15.6 鍊?

杩欓€熷害姣斿綋鍓嶇殑 SOTA 蹇?**鍑犱釜鏁伴噺绾?**锛屽悓鏃惰繕鎻愪緵鏇村ソ鐨勬€ц兘锛佸鏋滃叾浠栧洟闃熻兘澶熷鍒惰繖涓€鐐瑰苟涓旇繘鍏ュ紑婧愰鍩燂紝杩欏皢鏄法澶х殑杩涙锛屼絾鐩墠寰蒋缁濆鏄€岄仴閬ラ鍏堛€?

RetNet鐨勪富瑕佽础鐚彲浠ユ鎷负涓ゅぇ鐐?
- RetNet寮曞叆**澶氬昂搴︿繚鐣欐満鍒?**鏉ユ浛浠?**澶氬ご娉ㄦ剰鍔?**銆傝繖鏄秷闄よ嚜娉ㄦ剰鍔涙満鍒朵腑鐨勯瓟楝艰繖涓€缁勬垚閮ㄥ垎鐨勫叧閿€傚敖绠″姝わ紝杩欑淇濈暀鏈哄埗鏈変竴涓皬灏忕殑鐞嗚涓婄殑缂虹偣銆?
- RetNet 閫傜敤浜庝笁绉嶈绠楄寖寮忥紝鑰屽彧鏈変竴绉? Transformer 鍦ㄨ缁冨拰鎺ㄧ悊杩囩▼涓娇鐢ㄧ浉鍚岀殑搴忓垪澶勭悊鑼冨紡銆?
  - A. **骞惰**琛ㄧず浣胯缁冨苟琛屾€ц兘澶熷厖鍒嗗埄鐢? GPU 璁惧銆?
  - B. **寰幆**琛ㄧず鍦ㄥ唴瀛樺拰璁＄畻鏂归潰鍙疄鐜伴珮鏁堢殑 O(1) 鎺ㄧ悊銆傚彲浠ユ樉鐫€闄嶄綆閮ㄧ讲鎴愭湰鍜屽欢杩熴€傛澶栵紝鍦ㄦ病鏈夐敭鍊肩紦瀛樻妧宸х殑鎯呭喌涓嬶紝瀹炵幇涔熷緱鍒颁簡鏋佸ぇ鐨勭畝鍖栥€?
  - C. **鍒嗗潡寰幆**琛ㄧず鍙互鎵ц鏈夋晥鐨勯暱搴忓垪寤烘ā銆傚姣忎釜鏈湴鍧楄繘琛屽苟琛岀紪鐮佷互鎻愰珮璁＄畻閫熷害锛屽悓鏃跺鍏ㄥ眬鍧楄繘琛屽惊鐜紪鐮佷互鑺傜渷 GPU 鍐呭瓨銆?

鏂板瀷鍩虹缃戠粶鏋舵瀯 Retentive Network锛坄RetNet`锛夋垚鍔熺獊鐮翠簡鎵€璋撶殑鈥渀涓嶅彲鑳戒笁瑙抈鈥濋毦棰橈紝瀹炵幇浜哷甯曠疮鎵榒锛圥areto锛変紭鍖栥€?
- RetNet 鍦ㄤ繚鎸佽壇濂界殑鎵╁睍鎬ц兘鍜屽苟琛岃缁冪殑鍚屾椂锛屽疄鐜颁簡浣庢垚鏈儴缃插拰楂樻晥鐜囨帹鐞嗐€?

RetNet 鎺ㄧ悊鎴愭湰涓庢ā鍨嬪簭鍒楅暱搴︽棤鍏筹紝杩欒〃绀烘棤璁烘槸澶勭悊闀挎枃鏈簭鍒楋紝杩樻槸闀垮浘鍍忓簭鍒楋紝浜︽垨鏄湭鏉ユ洿闀跨殑闊宠棰戝簭鍒楋紝RetNet 閮藉彲浠ヤ繚鎸佺ǔ瀹氱殑楂樻晥鎺ㄧ悊銆?


### 寰蒋 BitNet

銆?2024-2-29銆慬BitNet b1.58锛氬紑鍚?1-bit澶ц瑷€妯″瀷鏃朵唬](https://mp.weixin.qq.com/s?__biz=MzAwMTA3MzM4Nw==&mid=2649498640&idx=1&sn=a860101ceee6bc3a777f465bdd1586da&chksm=82c7cd94b5b0448231f0017d2694e59f6e41369ea14a38a3a19a32a9ba18c3fe0f934e214bee&scene=21#wechat_redirect)

寰蒋浜氭床鐮旂┒闄㈡帹鍑轰簡 1-bit LLM 鏂板彉浣擄細`BitNet b1.58`銆?
- 璁烘枃鏍囬锛歔The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits](https://arxiv.org/pdf/2402.17764.pdf)

璇ユā鍨嬫瘡涓弬鏁颁粎浣跨敤涓夊€艰〃绀猴紝鍗?-1, 0 鎴? 1銆傚洜姝わ紝鍦? LLM 鐨勭煩闃典箻娉曟搷浣滀腑鍙渶瑕佹暣鏁板姞娉曪紝鑰屼笉闇€瑕佷换浣曟诞鐐规暟涔樻硶鎴栧姞娉曘€傚湪璇█妯″瀷鍥版儜搴﹀拰涓嬫父浠诲姟鎬ц兘鐨勮瘎浼颁腑
- BitNet b1.58 鑳藉涓庡叿鏈夌浉鍚屽弬鏁伴噺鍜岃缁冩暟鎹噺鐨勫叏绮惧害锛堝嵆FP16鎴朆F16锛塗ransformer LLM 鐩稿尮鏁屻€?
- 涓庢鍚屾椂锛屽畠鍦ㄩ€熷害銆佸唴瀛樹娇鐢ㄣ€佸悶鍚愰噺鍜岃兘鑰楃瓑鏂归潰鍏锋湁澶у箙浼樺娍銆?

BitNet b1.58 涓鸿缁冩柊涓€浠ｉ珮鎬ц兘楂樻晥鐜囩殑 LLMs 纭珛浜嗘柊鐨?**鎵╁睍瀹氬緥**锛坰caling law锛夊拰鏂规硶銆傛澶栧紩棰嗕簡涓€绉嶅叏鏂扮殑璁＄畻鑼冨紡锛屽苟涓哄紑鍙戜笓涓? 1-bit LLMs 浼樺寲鐨勭‖浠惰澶囬摵骞充簡閬撹矾銆?

BitNet 鏄涓€涓敮鎸佽缁?1姣旂壒澶ц瑷€妯″瀷鐨勬柊鍨嬬綉缁滅粨鏋勶紝鍏锋湁寮哄ぇ鐨勫彲鎵╁睍鎬у拰绋冲畾鎬э紝鑳藉鏄捐憲鍑忓皯澶ц瑷€妯″瀷鐨勮缁冨拰鎺ㄧ悊鎴愭湰銆?

涓庢渶鍏堣繘鐨?8姣旂壒閲忓寲鏂规硶鍜屽叏绮惧害 Transformer 鍩虹嚎鐩告瘮锛孊itNet 鍦ㄥぇ骞呴檷浣庡唴瀛樺崰鐢ㄥ拰璁＄畻鑳借€楃殑鍚屾椂锛岃〃鐜板嚭浜嗘瀬鍏风珵浜夊姏鐨勬€ц兘銆?

姝ゅ锛孊itNet 鎷ユ湁涓庡叏绮惧害 Transformer 鐩镐技鐨?**瑙勬ā娉曞垯**锛圫caling Law锛夛紝鍦ㄤ繚鎸佹晥鐜囧拰鎬ц兘浼樺娍鐨勫悓鏃讹紝杩樺彲浠ユ洿鍔犻珮鏁堝湴灏嗗叾鑳藉姏鎵╁睍鍒版洿澶х殑璇█妯″瀷涓婏紝浠庤€岃1姣旂壒澶ц瑷€妯″瀷锛?1-bit LLM锛夋垚涓哄彲鑳姐€?

### 寰蒋 YOCO

銆?2024-5-13銆慬YOCO锛氭墦鐮翠紶缁烡ecoder-only鏋舵瀯锛屽唴瀛樻秷鑰椾粎涓篢ransformer鐨勫叚鍒嗕箣涓€](https://mp.weixin.qq.com/s/X4HSyEreN4L4xTizC-_mow)

妯″瀷鏋舵瀯杩樺彧鏈変笁澶х被锛欴ecoder-Only銆丒ncoder-Only銆丒ncoder-Decoder銆?

寰蒋浜氭床鐮旂┒闄㈡帹鍑轰簡涓€绉嶅垱鏂版€х殑 Decoder-Decoder 鏋舵瀯 `YOCO`锛圷ou Only Cache Once锛夈€傞€氳繃**鑷В鐮佸櫒**鍜?**浜ゅ弶瑙ｇ爜鍣?**鐨勭嫭鐗规灦鏋勶紝YOCO 浠呴渶缂撳瓨涓€娆￠敭鍊煎锛屼粠鑰屾樉钁楅檷浣? GPU 鍐呭瓨鐨勪娇鐢ㄣ€?
- 璁烘枃 [You Only Cache Once: Decoder-Decoder Architectures for Language Models](https://arxiv.org/abs/2405.05254)

妯″瀷璇勪及涓紝YOCO 灞曠幇鍑轰笌鍚岃妯? Transformer 妯″瀷鐩稿缇庣殑鎬ц兘锛屽苟鍦ㄨ瑷€寤烘ā璇勪及銆佹ā鍨嬪ぇ灏忔墿灞曚互鍙婇暱涓婁笅鏂囧鐞嗘柟闈㈠叿鏈夋樉钁椾紭鍔裤€傜壒鍒槸鍦ㄩ檷浣? GPU 鍐呭瓨鍗犵敤鍜岀缉鐭濉厖寤惰繜鏂归潰锛?

YOCO 鏁翠綋鏋舵瀯璁捐濡備笅锛屽垎涓篳鑷В鐮佸櫒`锛圫elf-Decoder锛夊拰`浜ゅ弶瑙ｇ爜鍣╜锛圕ross-Decoder锛変袱閮ㄥ垎銆?

YOCO 瀹炵幇浜嗏€?**妯″瀷瓒婂ぇ锛屽唴瀛樿秺鐪?**鈥濓紝涓鸿嚜鐒惰瑷€澶勭悊棰嗗煙甯︽潵浜嗗叏鏂扮殑鐮旂┒鍜屽簲鐢ㄨ寖寮忋€?
- YOCO 浠呯紦瀛樹竴娆￠敭鍊煎锛屽彲澶у箙闄嶄綆 GPU 鍐呭瓨闇€姹傦紝涓斾繚鐣欏叏灞€娉ㄦ剰鍔涜兘鍔涖€?

鎵撶牬 GPT 绯诲垪寮€鍒涚殑 `Decoder-Only` 鏋舵瀯鈥斺€旀彁鍑? `Decoder-Decoder` 鏂板瀷鏋舵瀯锛屽悕涓? `YOCO` (You Only Cache Once)銆?
- 鍦ㄥ鐞? 512K 涓婁笅鏂囬暱搴︽椂锛屾爣鍑? Transformer 鍐呭瓨浣跨敤鏄? YOCO 鐨?6.4鍊嶏紝棰勫～鍏呭欢杩熸槸 YOCO 鐨?30.3鍊嶏紝鑰? YOCO 鐨勫悶鍚愰噺鎻愬崌鍒版爣鍑? Transformer 鐨?9.6鍊嶃€?


## 浣嶇疆缂栫爜鏂瑰紡



### 2021.3.23 Roformer

銆?2021-3-23銆慠otary Transformer锛岀畝绉? `RoFormer`锛屾槸杩戒竴绉戞妧`鑻忓墤鏋梎鑷爺鐨勮瑷€妯″瀷涔嬩竴锛屼富瑕佹槸涓篢ransformer缁撴瀯璁捐浜嗘柊鐨刞鏃嬭浆寮忎綅缃紪鐮乣锛圧otary Position Embedding锛宍RoPE`锛夈€?
- `RoPE`鍏锋湁鑹ソ鐨勭悊璁烘€ц川锛屼笖鏄洰鍓?**鍞竴**涓€绉嶇敤鍒扮嚎鎬ttention鐨勭粷瀵逛綅缃紪鐮侊紝鐩墠鏉ョ湅瀹為獙缁撴灉涔熼涓轰笉閿欍€?
- 鍙傝€冮厤缃細鍦?24G鏄惧瓨鐨?3090涓婏紝璺憁axlen=1024锛宐atch_size鑳借窇鍒?8浠ヤ笂銆?

璇︾粏浠嬬粛锛?
- [Transformer鍗囩骇涔嬭矾锛?2銆佸崥閲囦紬闀跨殑鏃嬭浆寮忎綅缃紪鐮乚(https://kexue.fm/archives/8265)

浣跨敤

- [pytorch鐗堟湰](https://github.com/JunnYu/RoFormer_pytorch)
- huggingface [roformer](https://huggingface.co/docs/transformers/model_doc/roformer)

```py
from transformers import RoFormerTokenizerFast

tokenizer = RoFormerTokenizerFast.from_pretrained("junnyu/roformer_chinese_base")
tokenizer.tokenize("浠婂ぉ澶╂皵闈炲父濂姐€?")
```


## 妫€绱㈠寮?

澧炲ぇ妯″瀷骞朵笉鏄彁鍗囨€ц兘鐨勫敮涓€璺緞锛岀敤涓€绉嶆悳绱?/鏌ヨ淇℃伅鐨勬柟寮忔潵澧炲己妯″瀷锛屽皬鐨勭敓鎴愯瑷€妯″瀷涔熻兘杈惧埌涔嬪墠澶фā鍨嬫墠鑳借揪鍒扮殑鎬ц兘銆?

璇█妯″瀷鐨勪换鍔℃槸鍋?**濉┖棰?**锛岃繖瀵逛簬璇█淇℃伅鏈夋剰涔夛紝浣嗘槸瀵逛簬浜嬪疄淇℃伅鍜屼笘鐣岀煡璇嗕俊鎭槸鏃犳晥鐨勩€?
- 鏈夋椂闇€瑕佷笌浜嬪疄鏈夊叧鐨勪俊鎭?

浠ｈ〃
- DeepMind 鐨? RETRO Transformer
  - DeepMind 鐨? RETRO锛圧etrieval-Enhanced TRansfOrmer锛夋ā鍨嬨€傝妯″瀷涓? GPT-3 鎬ц兘鐩稿綋锛屼絾鍙傛暟閲忎粎涓? GPT-3 鐨? 4%銆?
- OpenAI 鐨? WebGPT


### 2021.12.16 WebGPT

OpenAI 鎺ㄥ嚭 WebGPT, 瑙ｅ喅 long-form quesion-answering (LFQA) 鐨勬柟妗?, 寮€鏀惧煙QA鍥炲鏇撮暱鏇村彲闈犮€?
- [WebGPT: Improving the factual accuracy of language models through web browsing](https://openai.com/research/webgpt)
- [WebGPT绠€璇籡(https://zhuanlan.zhihu.com/p/591565418)
- 姣? InstructGPT 鎻愬嚭绋嶆棭涓€浜?

WebGPT 鎬濊矾绫讳技 Knowledge-Grounded Conversation锛屽埄鐢ㄦ悳绱㈠紩鎿庡仛鐩稿叧鏂囨。妫€绱紝浠庤€岀敓鎴愭洿闀跨殑绛旀銆備富瑕佺殑涓や釜璐＄尞锛?
- 寰皟鐨勮瑷€妯″瀷鍙互涓庝竴涓熀浜庢枃鏈殑Web娴忚鐜浜や簰锛屼粠鑰屽彲浠ョ鍒扮鍦颁娇鐢ㄦā浠垮拰寮哄寲瀛︿範浼樺寲妫€绱㈠拰鑱氬悎鏁堟灉銆?
- 鍙傝€僕eb妫€绱㈠嚭鏉ョ殑淇℃伅鐢熸垚鍥炲銆俵abeler鍙互鏍规嵁妫€绱㈠嚭鏉ョ殑淇℃伅鍒ゆ柇factual鍑嗙‘鐜囷紝闄嶄綆浜嗙嫭绔嬭皟鐮旈棶棰樻纭€х殑闅惧害銆?

杩欎釜鎯虫硶骞堕潪 WebGPT棣栨鎻愬嚭
- 2021骞村垵, Facebook (FAIR) 灏辨彁鍑轰娇鐢ㄦ悳绱㈠紩鎿庢潵鎻愬崌瀵硅瘽鍥炲鐨勮川閲忥細ACL2022 [Internet-Augmented Dialogue Generation](https://aclanthology.org/2022.acl-long.579/)

WebGPT 鎬濊矾鏇磋繘涓€姝ワ紝瀹屽叏妯℃嫙浜嗕汉浣跨敤鎼滅储寮曟搸鐨勬柟娉?(鏈夋洿澶歛ction: 鎼滅储銆佺偣鍑汇€佺炕椤点€佸洖閫€绛夌瓑)锛岃€岄潪浠呯敓鎴恠earch query骞朵娇鐢ㄥ叾缁撴灉銆?

### 2022.2.7 RETRO

DeepMind 鎺ㄥ嚭 RETRO, 鏁村悎浜嗕粠鏁版嵁搴撲腑妫€绱㈠埌鐨勪俊鎭紝灏嗗叾鍙傛暟浠庢槀璐电殑浜嬪疄鍜屼笘鐣岀煡璇嗗瓨鍌ㄤ腑瑙ｆ斁鍑烘潵銆?
- 璁烘枃: [Improving language models by retrieving from trillions of tokens](https://arxiv.org/pdf/2112.04426.pdf)
- [illustrated-retrieval-transformer](http://jalammar.github.io/illustrated-retrieval-transformer)
- 銆?2022-1-4銆慬鍙傛暟閲忎粎涓?4%锛屾€ц兘濯茬編GPT-3锛氬紑鍙戣€呭浘瑙eepMind鐨凴ETRO](https://www.jiqizhixin.com/articles/2022-01-04-8)

鍔犲叆妫€绱㈡柟娉曚箣鍚庯紝璇█妯″瀷鍙互缂╁皬寰堝銆?
- 绁炵粡鏁版嵁搴撳彲浠ュ府鍔╂ā鍨嬫绱㈠畠闇€瑕佺殑浜嬪疄淇℃伅銆?
- ![](https://image.jiqizhixin.com/uploads/editor/ffbea1f3-54eb-411d-a9a9-3c0912dfef3c/1641280248346.png)

#### 妯″瀷缁撴瀯

缁撴瀯
- RETRO 鏄? **缂栫爜鍣? - 瑙ｇ爜鍣?**妯″瀷锛屽儚鍘熷鐨? Transformer銆?
- 鐒惰€屽湪妫€绱㈡暟鎹簱鐨勫府鍔╀笅澧炲姞浜?**杈撳叆搴忓垪**銆?
- 璇ユā鍨嬪湪鏁版嵁搴撲腑鎵惧埌鏈€鍙兘鐨勫簭鍒楋紝骞舵坊鍔犲埌杈撳叆涓€?
- RETRO 鍒╃敤瀹冪殑榄斿姏鐢熸垚杈撳嚭棰勬祴銆?
- ![](https://image.jiqizhixin.com/uploads/editor/96d18172-b521-4ed5-a913-a00440b05625/1641280241153.png)


#### RETRO 妫€绱㈡暟鎹簱

杩欓噷鐨勬暟鎹簱鏄竴涓?**閿€煎瓨鍌?**锛坘ey-value store锛夋暟鎹簱銆?
- key 鏄爣鍑嗙殑 **BERT 鍙ュ瓙宓屽叆**锛寁alue 鏄敱涓ら儴鍒嗙粍鎴愮殑**鏂囨湰**锛?
- Neighbor锛岀敤浜庤绠? key锛?
- Completion锛屽師鏂囦欢涓枃鏈殑寤剁画銆?

RETRO 鏁版嵁搴撳寘鍚熀浜? MassiveText 鏁版嵁闆嗙殑 2 涓囦嚎涓璇█ token銆俷eighbor chunk 鍜? completion chunk 鐨勯暱搴︽渶澶氫负 64 涓? token銆?
- ![](https://image.jiqizhixin.com/uploads/editor/713760aa-cf75-4bc7-8116-e308ce3b8b83/1641280228557.png)

#### 鏁版嵁搴撴煡鎵?

杩涘叆 RETRO 鍓?
- 杈撳叆鎻愮ず杩涘叆 BERT銆傚杈撳嚭鐨勪笂涓嬫枃鍚戦噺杩涜**骞冲潎**浠ユ瀯寤哄彞瀛愬祵鍏ュ悜閲忋€?
  - ![](https://image.jiqizhixin.com/uploads/editor/3e8b9491-570a-4280-b36a-e68a6d0fff7c/1641280220663.png)
- 鐒跺悗锛屼娇鐢ㄨ鍚戦噺鏌ヨ鏁版嵁搴撱€傝繎浼兼渶杩戦偦鎼滅储銆傛绱袱涓渶杩戦偦
  - ![](https://image.jiqizhixin.com/uploads/editor/aac2a845-a303-415b-b582-7b55402db078/1641280209906.png)
- 灏嗚繖浜涙坊鍔犲埌璇█妯″瀷鐨勮緭鍏ヤ腑
  - 妫€绱㈠嚭鐨勬枃鏈垚涓? RETRO 杈撳叆鐨勪竴閮ㄥ垎锛孴ransformer 鍜? RETRO 鍧楀皢淇℃伅鍚堝苟鍒板畠浠殑澶勭悊涓?
  - ![](https://image.jiqizhixin.com/uploads/editor/ff98762d-0d34-4771-8753-56d6b7762648/1641280203796.png)


#### 楂樺眰娆＄殑 RETRO 鏋舵瀯

RETRO 鏋舵瀯鐢变竴涓?**缂栫爜鍣?**鍫嗘爤鍜屼竴涓?**瑙ｇ爜鍣?**鍫嗘爤缁勬垚銆?
- 缂栫爜鍣ㄧ敱鏍囧噯鐨? Transformer 缂栫爜鍣ㄥ潡锛坰elf-attention + FFNN锛夌粍鎴愩€俁etro 浣跨敤鐢变袱涓? Transformer 缂栫爜鍣ㄥ潡缁勬垚鐨勭紪鐮佸櫒銆?
  - 缂栫爜鍣ㄥ爢鏍堜細澶勭悊妫€绱㈠埌鐨勮繎閭伙紝鐢熸垚鍚庣画灏嗙敤浜庢敞鎰忓姏鐨? KEYS 鍜? VALUES 鐭╅樀
- 瑙ｇ爜鍣ㄥ爢鏍堝寘鍚簡涓ょ瑙ｇ爜鍣? block锛?
  - 鏍囧噯 Transformer 瑙ｇ爜鍣ㄥ潡锛圓TTN + FFNN锛?
  - RETRO 瑙ｇ爜鍣ㄥ潡锛圓TTN + Chunked cross attention (CCA) + FFNN锛?
- 瑙ｇ爜鍣? block 鍍? GPT 涓€鏍峰鐞嗚緭鍏ユ枃鏈€傚鎻愮ず token 搴旂敤鑷敞鎰忓姏锛堝洜姝ゅ彧鍏虫敞涔嬪墠鐨? token锛夛紝鐒跺悗閫氳繃 FFNN 灞傘€傚彧鏈夊埌杈? RETRO 瑙ｇ爜鍣ㄦ椂锛屽畠鎵嶅紑濮嬪悎骞舵绱㈠埌鐨勪俊鎭€備粠 9 寮€濮嬬殑姣忎釜绗笁涓? block 鏄竴涓? RETRO block锛堝厑璁稿叾杈撳叆鍏虫敞杩戦偦锛夈€傛墍浠ョ 9銆?12銆?15鈥?32 灞傛槸 RETRO block銆?
- ![](https://image.jiqizhixin.com/uploads/editor/5103886f-035d-4506-9e03-32b9ec93259b/1641280193608.png)
- ![](https://image.jiqizhixin.com/uploads/editor/305626c2-7918-419a-9e4c-5c8d7eaf0e60/1641280182910.png)




## 杈撳叆杈撳嚭 鏀硅繘


杈撳叆闀垮害鏀硅繘

### 2023.7.8 LongNet

銆?2023-7-8銆慬1000000000锛佸井杞敼杩汿ransformer涓€娆¤兘璁颁綇杩欎箞澶歵oken浜哴(https://mp.weixin.qq.com/s/PKKC4lMdSTg-ButNnZHLlw)
- 鏈€寮虹殑GPT-4涔熸墠鏈€澶ф敮鎸佷竴娆″鐞?32k token锛岀浉褰撲簬50椤垫枃瀛椼€?
- 鑰岃兘澶熷彧鐢?1鍒嗛挓鐪嬪畬涓€鏈暟涓囧瓧灏忚鐨凜laude锛屽叾token鏁颁篃涓嶈繃鈥滄墠鈥?100k锛?10涓囷級銆?

涓€娆℃€ф墿灞曞埌10浜匡紝骞朵笖杩欎釜鏁板瓧鐞嗚涓婂叾瀹炶繕鏄棤闄愮殑锛岃繖涓嶅氨鎰忓懗鐫€锛氫笉涔呯殑灏嗘潵锛屾暣涓鏂欏簱鐢氳嚦浜掕仈缃戦兘鑳借涓轰竴涓簭鍒楋紵

浣滆€呮彁鍑轰竴涓猅ransformer鍙樹綋锛歚LongNet`锛屽畠搴旂敤浜嗕竴绉嶅彨鍋氣€?**鑶ㄨ儉娉ㄦ剰鍔?**锛坉ilated attention锛夆€濈殑鏈哄埗锛屽彲浠ラ殢鐫€璺濈鐨勫闀匡紝璁╂敞鎰忓姏鍦猴紙妯″瀷鎰熺煡鑼冨洿锛夊憟鎸囨暟绾ф墿灞曘€?

鍏蜂綋鑰岃█锛宒ilated attention鏇夸唬浜嗘櫘閫歍ransformer涓殑娉ㄦ剰鍔涙満鍒剁殑锛屽叾涓€鑸殑璁捐鍘熷垯鏄細
> 璁╂敞鎰忓姏鐨勫垎閰嶉殢鐫€token涔嬮棿璺濈鐨勫闀匡紝鍛堟寚鏁扮骇涓嬮檷銆?

dilated attention鑳藉浜х敓绾挎€ц绠楀鏉傚害鍜宼oken涔嬮棿鐨勫鏁颁緷璧栨€э紝浠庤€岃В鍐充簡娉ㄦ剰鍔涜祫婧愭湁闄愶紝浣嗘瘡涓€涓猼oken閮藉彲璁块棶鐨勭煕鐩俱€?


## MLP 鏀硅繘

澶氬眰鎰熺煡鍣紙MLP锛夎绉颁负**鍏ㄨ繛鎺ュ墠棣?**绁炵粡缃戠粶锛屾槸褰撲粖娣卞害瀛︿範妯″瀷鐨勫熀纭€鏋勫缓鍧椼€?

MLP 閲嶈鎬ф棤璁烘€庢牱寮鸿皟閮戒笉涓鸿繃锛屾槸鏈哄櫒瀛︿範涓敤浜庨€艰繎闈炵嚎鎬у嚱鏁扮殑榛樿鏂规硶銆?

鐒惰€岋紝MLP 鏄惁鏈€浣抽潪绾挎€у洖褰掑櫒鍛紵

灏界 MLP 琚箍娉涗娇鐢紝浣嗗瓨鍦ㄦ槑鏄剧己闄枫€?
- 渚嬪锛屽湪 Transformer 妯″瀷涓紝MLP 鍑犱箮娑堣€椾簡鎵€鏈夐潪宓屽叆寮忓弬鏁帮紝骞朵笖閫氬父鍦ㄦ病鏈夊悗澶勭悊鍒嗘瀽宸ュ叿鐨勬儏鍐典笅锛岀浉瀵逛簬娉ㄦ剰鍔涘眰鏉ヨ锛屽畠浠殑鍙В閲婃€ц緝宸€?

### KAN

銆?2024-5-3銆慬Transformer瑕佸彉Kansformer锛熺敤浜嗗嚑鍗佸勾鐨凪LP杩庢潵鎸戞垬鑰匥AN](https://www.jiqizhixin.com/articles/2024-05-03-3)

MIT 鎻愬嚭鐨? KAN 鐏垫劅鏉ユ簮浜? Kolmogorov-Arnold 琛ㄧず瀹氱悊鐨勭綉缁溿€?
- 璁烘枃锛歔KAN: Kolmogorov-Arnold Networks](https://arxiv.org/pdf/2404.19756)
- Github锛歔pykan](https://github.com/KindXiaoming/pykan)

KAN 鍦ㄥ噯纭€у拰鍙В閲婃€ф柟闈㈣〃鐜颁紭浜? MLP锛岃€屼笖鑳戒互闈炲父灏戠殑鍙傛暟閲忚儨杩囦互鏇村ぇ鍙傛暟閲忚繍琛岀殑 MLP銆?

鏈夌爺绌惰€呭皢 KAN 鍒涙柊鏋舵瀯鐨勭悊蹇垫墿灞曞埌鍗风Н绁炵粡缃戠粶锛屽皢鍗风Н鐨勭粡鍏哥嚎鎬у彉鎹㈡洿鏀逛负姣忎釜鍍忕礌涓彲瀛︿範鐨勯潪绾挎€ф縺娲诲嚱鏁帮紝鎻愬嚭骞跺紑婧? KAN 鍗风Н锛圕KAN锛?
- 銆?2024-5-20銆慬鏇夸唬MLP鐨凨AN锛岃寮€婧愰」鐩墿灞曞埌鍗风Н浜哴(https://www.jiqizhixin.com/articles/2024-05-20-2)
- [Convolutional-KANs](https://github.com/AntonioTepsich/Convolutional-KANs)

Kolmogorov 1957 骞村氨鍙戠幇浜?**澶氬眰**绁炵粡缃戠粶锛屾瘮 Rumerhart銆丠inton 鍜? William 鐨? 1986 骞磋鏂囧彂琛ㄧ殑鏃堕棿瑕佹棭寰楀锛屼絾浠栧嵈琚タ鏂瑰拷瑙嗕簡銆?

涓€绉嶆湁鍓嶆櫙鐨勫灞傛劅鐭ュ櫒锛圡LP锛夌殑鏇夸唬鏂规锛岀О涓? Kolmogorov-Arnold Networks锛圞AN锛夈€?
- MLP 鐨勮璁＄伒鎰熸潵婧愪簬`閫氱敤杩戜技瀹氱悊` 锛堥€氱敤閫艰繎瀹氱悊锛?
- 鑰? KAN 璁捐鐏垫劅鍒欐潵婧愪簬 `Kolmogorov-Arnold 琛ㄧず瀹氱悊`銆?

Kolmogorov-Arnold 琛ㄧず瀹氱悊
- Vladimir Arnold 鍜? Andrey Kolmogorov 璇佹槑浜嗗鏋? f 鏄竴涓湪鏈夌晫鍩熶笂鐨?**澶氬彉閲忚繛缁嚱鏁?**锛岄偅涔? f 鍙互鍐欐垚涓€涓?**鍗曞彉閲忚繛缁嚱鏁?**鍜?**浜屽厓鍔犳硶杩愮畻**鐨勬湁闄愮粍鍚堛€?

涓? MLP 绫讳技锛孠AN 鎷ユ湁**鍏ㄨ繛鎺?**缁撴瀯銆傝€? MLP 鍦ㄨ妭鐐癸紙绁炵粡鍏冿級涓婃斁缃浐瀹氭縺娲诲嚱鏁帮紝KAN 鍒欏湪杈癸紙鏉冮噸锛変笂鏀剧疆鍙涔犵殑婵€娲诲嚱鏁般€?

鍥犳锛孠AN **瀹屽叏娌℃湁绾挎€ф潈閲嶇煩闃?**锛? [瀵规瘮鍥綸(https://image.jiqizhixin.com/uploads/editor/2ea4a752-4eb5-4bd7-a21f-1f228efcc427/640.png)
- 姣忎釜鏉冮噸鍙傛暟閮借鏇挎崲涓轰竴涓彲瀛︿範鐨勪竴缁村嚱鏁帮紝鍙傛暟鍖栦负**鏍锋潯**锛坰pline锛夈€?
- KAN 鐨勮妭鐐逛粎瀵逛紶鍏ヤ俊鍙疯繘琛屾眰鍜岋紝鑰屼笉搴旂敤浠讳綍闈炵嚎鎬у彉鎹€€?
- ![瀵规瘮鍥綸(https://image.jiqizhixin.com/uploads/editor/2ea4a752-4eb5-4bd7-a21f-1f228efcc427/640.png)

灏界 KAN 鏁板瑙ｉ噴鑳藉姏涓嶉敊锛屼絾瀹為檯涓婂彧鏄?**鏍锋潯**鍜? **MLP** 鐨勭粍鍚堬紝鍒╃敤浜嗕簩鑰呯殑浼樼偣锛岄伩鍏嶄簡缂虹偣鐨勫嚭鐜般€?
- 鏍锋潯鍦ㄤ綆缁村嚱鏁颁笂鍑嗙‘搴﹂珮锛屾槗浜庡眬閮ㄨ皟鏁达紝骞朵笖鑳藉鍦ㄤ笉鍚屽垎杈ㄧ巼涔嬮棿鍒囨崲銆傜劧鑰岋紝鐢变簬鏍锋潯鏃犳硶鍒╃敤缁勫悎缁撴瀯锛屽洜姝ゅ瓨鍦ㄤ弗閲? COD 闂銆?
- 鍙︿竴鏂归潰锛孧LP 鐢变簬鍏剁壒寰佸涔犺兘鍔涳紝杈冨皯鍙楀埌 COD 鐨勫奖鍝嶏紝浣嗗湪浣庣淮绌洪棿涓嵈涓嶅鏍锋潯鍑嗙‘锛屽洜涓哄畠浠棤娉曚紭鍖栧崟鍙橀噺鍑芥暟銆?

KAN 鐨勬渶澶х摱棰?: 璁粌閫熷害鎱€€?
- 鐩稿悓鏁伴噺鐨勫弬鏁颁笅锛孠AN 鐨勮缁冭€楁椂閫氬父鏄? MLP 鐨? 10 鍊嶃€?
- KAN 璁粌閫熷害鎱㈡洿鍍忔槸涓€涓湭鏉ュ彲浠ユ敼杩涚殑宸ョ▼闂锛岃€屼笉鏄竴涓牴鏈€х殑闄愬埗

## Attention 鏀硅繘


### QKV

MHA銆丟QA銆丮QA銆丮LA 鍘熺悊瀵规瘮
- 浼犵粺 Transformer 閲囩敤 MHA锛屼絾 KV Cache 鍦ㄦ帹鐞嗚繃绋嬩腑鍙兘鎴愪负鎬ц兘鐡堕銆?
- `MQA` 鍜? `GQA` 铏界劧鍦ㄤ竴瀹氱▼搴︿笂鍙互鍑忓皯KV Cache鐨勫崰鐢紝浣嗘晥鏋滈€氬父涓嶅 `MHA`銆?
- `MLA` 閫氳繃浣庣З Key-Value鑱斿悎鍘嬬缉鎶€鏈紝涓嶄粎瀹炵幇浜嗘瘮`MHA`鏇翠紭鐨勬晥鏋滐紝杩樺ぇ骞呭噺灏戜簡鎵€闇€鐨凨V Cache澶у皬銆?


#### GQA: Grouped-Query Attention

Grouped-Query Attention 锛氬浜庢洿澶у弬鏁伴噺銆佹洿澶х殑 context length銆佹洿澶х殑 batchsize 鏉ヨ锛屽師濮嬬殑MHA锛坢ulti-head attention锛夌殑鍐呭瓨鍗犵敤浼氭洿楂橈紙鍥犱负鍦ㄨ绠楁椂瑕佺紦瀛榩re token鐨凨銆乂鐭╅樀锛夈€?
- MQA锛坢ulti-query attention锛夎鎵€鏈夌殑 head 鍏变韩 1 涓? KV projection 鐭╅樀锛?
- GQA锛坓rouped-query attention 锛変娇鐢? 8 涓? KV projections锛堥€夋嫨8鏄洜涓篈100 8GPUs锛? 鏉ュ噺灏戝唴瀛樺崰鐢ㄣ€?

鍦? 30B 妯″瀷涓婅缁? 150B tokens锛屽彂鐜? GQA 鏁堟灉鍜? MHA 宸笉澶氾紝姣? MQA 瑕佸ソ锛涘湪 1 涓猲ode鐨? 8 涓? A100 GPUs 涓婃帹鐞嗛€熷害 GQA 鍜? MQA宸笉澶氾紝姣? MHA 瑕佸ソ锛圡QA 鍦ㄦ帹鐞嗙殑鏃跺€欙紝瑕佹妸 KV projections 澶嶅埗鍒?8寮犲崱涓婏級銆?

#### MQA: Muti Query Attention

MQA 鏄? 2019 骞存彁鍑虹殑涓€绉嶆柊鐨? Attention 鏈哄埗锛屽叾鑳藉鍦ㄤ繚璇佹ā鍨嬫晥鏋滅殑鍚屾椂鍔犲揩 decoder 鐢熸垚 token 鐨勯€熷害銆?
- 璁烘枃锛? [Fast Transformer Decoding: One Write-Head is All You Need](https://arxiv.org/pdf/1911.02150.pdf)
- 鎵€鏈? head 涔嬮棿**鍏变韩**涓€浠? key 鍜? value 鐨勫弬鏁?

MQA 鍦? encoder 涓婄殑鎻愰€熸病鏈夐潪甯告槑鏄撅紝浣嗗湪 decoder 涓婄殑鎻愰€熸槸寰堟樉钁楃殑
- ![](https://pic1.zhimg.com/80/v2-150a48c2eadeacd0aca50408ea391710_1440w.webp)

Multi Query Attention锛圡QA锛? 鍜? Multi Head Attention锛圡HA锛夊彧宸簡涓€涓崟璇嶏紝浠庛€孒ead銆嶅彉鎴愪簡銆孮uery銆嶃€?

MQA 璁?**鎵€鏈夌殑澶翠箣闂? 鍏变韩 鍚屼竴浠? Key 鍜? Value 鐭╅樀**锛屾瘡涓ご鍙崟鐙繚鐣欎簡涓€浠? Query 鍙傛暟锛屼粠鑰屽ぇ澶у噺灏? Key 鍜? Value 鐭╅樀鐨勫弬鏁伴噺銆?
- 銆屽弬鏁板叡浜€嶅苟涓嶆槸鏂板鎬濊矾锛孉lbert 閫氳繃浣跨敤**璺ㄥ眰鍏变韩鍙傛暟**锛圕ross-layer parameter sharing锛夋柟寮忔潵澶уぇ鍑忓皯 bert 鐨勫弬鏁伴噺
- MQA 瀹為檯涓婃槸灏? head 涓殑 key 鍜? value 鐭╅樀鎶藉嚭鏉ュ崟鐙瓨涓轰竴浠藉叡浜弬鏁帮紝鑰? query 鍒欐槸渚濇棫淇濈暀鍦ㄥ師鏉ョ殑 head 涓紝姣忎釜 head 鏈変竴浠借嚜宸辩嫭鏈夌殑 query 鍙傛暟銆?

浠ｇ爜瑙乕鍘熸枃](https://zhuanlan.zhihu.com/p/634236135)


#### MLA: Multi-head Latent Attention


銆?2024-9-26銆慬娉ㄦ剰鍔涙満鍒剁殑鍙樹綋涔婱LA](https://mp.weixin.qq.com/s/dWZk8TBY89re207ZL3GjfA)

`MLA`(Multi-head Latent Attention) 鏄? 鏉窞**娣卞害姹傜储**浜哄伐鏅鸿兘鍦╜DeepSeek` V2 鎻愬嚭鐨勪竴绉?**娉ㄦ剰鍔涙満鍒跺彉浣?**銆?

MLA 瑙ｅ喅鎺ㄧ悊杩囩▼涓?, 鐢变簬attention鏈哄埗涓?**KV Cache鍗犵敤杩囧鍐呭瓨**鑰屽鑷寸殑鎬ц兘鐡堕闂銆?

MLA 寮曞叆浜?**浣庣ЗKV鍘嬬缉**鎶€鏈紝鏈夋晥鍑忓皯浜咾V Cache 澶у皬锛屼粠鑰岀紦瑙ｄ簡杩欎竴闂銆?
- 瀹樻柟鎶€鏈姤鍛奫浠嬬粛](https://arxiv.org/pdf/2405.04434v2)

`MLA` 閫氳繃浣庣З Key-Value鑱斿悎鍘嬬缉鎶€鏈紝涓嶄粎瀹炵幇浜嗘瘮`MHA`鏇翠紭鐨勬晥鏋滐紝杩樺ぇ骞呭噺灏戜簡鎵€闇€鐨凨V Cache澶у皬銆?

MLA閫氳繃浣庣З鑱斿悎鍘嬬缉key鍜寁alue鏉ュ噺灏慿v cache銆?

浠庢敞鎰忓姏鏈哄埗鐨勬楠ゆ潵鍒嗘瀽锛?
- 閫氳繃杈撳叆x涔樹互涓嶅悓鐭╅樀鍙傛暟Wq銆乄k銆乄v, 寰楀埌涓嶅悓鐨凲KV鍚戦噺
- 杞崲鍒癚KV鍚戦噺鏃讹紝灏唜涔樹互涓€涓綆绉╃煩闃碉紝寰楀埌浣庨樁鐭╅樀琛ㄧず
- 鍐嶉€氳繃楂橀樁鐭╅樀鏉ユ仮澶嶅師鏉ョ殑鐗瑰緛绌洪棿銆傜敱浜庣煩闃垫槸妯″瀷鐨勬潈閲嶅弬鏁板凡缁忎繚瀛橈紝鎵€浠ュ彧闇€瑕佷繚瀛樹竴涓綆绉╃殑娼滃眰鐗瑰緛灏卞彲浠ユ仮澶嶆垚KV锛岃€屼笉鏄儚涔嬪墠闇€瑕佸悓鏃剁紦瀛楰V銆?


涓轰粈涔圠oRA鎻愬嚭杩欎箞涔呬簡锛岀洿鍒? MLA 鎵嶆彁鍑哄KV Cache浣庣З鍒嗚В鐨勫仛娉??

### 鎺ㄧ悊鍔犻€?


#### 鑺墖

銆?2023-12-19銆戠編鍥借姱鐗囧垵鍒涘叕鍙? [Etched AI](https://www.etched.ai/) 瀹ｇО寮€鍒涗簡涓€椤规柊鐨勬妧鏈紝灏? Transformer 鏋舵瀯鐩存帴鈥滅儳褰曗€濆埌浜嗚姱鐗囦腑?锛屽垱閫犲嚭浜嗕笘鐣屼笂鏈€寮哄ぇ鐨勪笓闂ㄧ敤浜嶵ransformer鎺ㄧ悊鐨勬湇鍔″櫒銆傚彲浠ヨ繍琛屼竾浜垮弬鏁扮殑妯″瀷锛?? 鐢╄嫳浼熻揪icon鍑犵櫨鏉¤?
- ![](https://assets-global.website-files.com/6570a6bdf377183fb173431e/6570b5e6b0cd5f0189cf79b8_hero.webp)

灏? Transformer鏋舵瀯鐩存帴鈥滅儳褰曗€濆埌鑺墖涓紝杩欐剰鍛崇潃Transformer妯″瀷鐨勬帹鐞嗗彲浠ュ湪涓撻棬鐨勭‖浠朵笂杩愯锛岃€屼笉闇€瑕佷緷璧栦紶缁熺殑CPU鎴朑PU銆傝繖灏嗗ぇ澶ф彁楂樻帹鐞嗛€熷害锛岄檷浣庡姛鑰楋紝骞舵彁楂樻ā鍨嬬殑鎬ц兘銆?
- 瑙ｇ爜閫熷害杩滆秴 A100, H100: NVIDIA A100(1x) < NVIDIA H100(5x) < Etched Sohu(15+x)

鍔熻兘锛?
- ? **瀹炴椂**璇煶浠ｇ悊锛氳兘澶熷湪姣鍐呭鐞嗘垚鍗冧笂涓囩殑璇嶃€?
- ? 鏇村ソ鐨勭紪鐮佷笌**鏍戞悳绱?**锛氬彲浠ュ苟琛屾瘮杈冩暟鐧句釜鍝嶅簲銆?
- ? 澶氭挱鎺ㄦ祴瑙ｇ爜锛氬疄鏃剁敓鎴愭柊鍐呭銆?
- ? 杩愯鏈潵鐨勪竾浜垮弬鏁版ā鍨嬶細鍙渶涓€涓牳蹇冿紝鏀寔鍏ㄥ紑婧愯蒋浠舵爤锛屽彲鎵╁睍鑷?100T鍙傛暟妯″瀷銆?
- ? 楂樼骇瑙ｇ爜鎶€鏈細鍖呮嫭鍏夋潫鎼滅储鍜孧CTS瑙ｇ爜銆?
- ? 姣忎釜鑺墖144 GB HBM3E锛氭敮鎸丮oE鍜岃浆鎹㈠櫒鍙樹綋銆?

杩欏浜庤嫳浼熻揪鏉ヨ鏄法澶х殑鎸戞垬銆傝嫳浼熻揪涓€鐩存槸浜哄伐鏅鸿兘棰嗗煙鐨勯瀵艰€呬箣涓€锛屽叾GPU琚箍娉涘簲鐢ㄤ簬娣卞害瀛︿範妯″瀷鐨勮缁冨拰鎺ㄧ悊銆傜劧鑰岋紝Etched AI鐨勬妧鏈彲鑳芥敼鍙樿繖涓€鏍煎眬銆?

璇︾粏锛歩conetched.ai


#### TransNAR

鎷晳Transformer鎺ㄧ悊鑳藉姏DeepMind鏂扮爺绌讹紝TransNAR锛氱粰妯″瀷宓屽叆绠楁硶鎺ㄧ悊澶ц剳

銆?2024-6-19銆慏eepMind 璁烘枃鎻愬嚭鐢?**娣峰悎鏋舵瀯**鏂规硶锛岃В鍐砊ransformer妯″瀷鐨?**鎺ㄧ悊**缂洪櫡銆?
- 璁烘枃鍦板潃锛歔Transformers meet Neural Algorithmic Reasoners](https://arxiv.org/abs/2406.09308)

灏員ransformer鐨凬LU鎶€鑳戒笌鍩轰簬GNN鐨勭缁忕畻娉曟帹鐞嗗櫒锛圢AR锛夌殑寮哄ぇ绠楁硶鎺ㄧ悊鑳藉姏鐩哥粨鍚堬紝鍙互瀹炵幇鏇村姞娉涘寲銆佺ǔ鍋ャ€佸噯纭殑LLM鎺ㄧ悊銆?
- TransNAR锛氱敤棰勮缁僋AR澧炲己Transformer
- ![](http://lib.ia.ac.cn:8003/ContentDelivery/20240619/06zc2.05_879FCE72BC2CB9C3039E5FC2ADFE91C3.png)

绁炵粡绠楁硶鎺ㄧ悊锛圢AR锛夌敱浣滆€呬箣涓€Petar Veleckovic, 2021骞翠笌浜哄悎钁楃殑涓€绡囪鏂囦腑鎻愬嚭锛屽苟琚帴鏀朵负Patterns鏈熷垔鐨刼pinion paper銆?
- 璁烘枃鍦板潃锛歔Neural Algorithmic Reasoning](https://arxiv.org/abs/2105.02761)

NAR琚О涓恒€屾瀯寤鸿兘鎵ц绠楁硶鐨勭缁忕綉缁滅殑鑹烘湳銆嶃€傜畻娉曚笌娣卞害瀛︿範鐨勬湰璐ㄤ笉鍚岋紝浣嗗鏋滅缁忕綉缁滆兘澶熸洿濂藉湴妯′豢绠楁硶锛屽畠鐢氳嚦鍙兘鍏峰绠楁硶鐨勫己娉涘寲鎬с€?

NAR 鏁翠綋鎯虫硶: 
- 璁粌涓€涓珮缁撮殣绌洪棿涓殑澶勭悊鍣ㄧ綉缁淧锛坧rocessor network锛夛紝鏃ㄥ湪涓嶆柇閫艰繎绠楁硶鐨勮繍琛岀粨鏋淎(x)銆?
- 浣嗙敱浜庣畻娉曠殑杈撳叆鍜岃緭鍑轰竴鑸槸鍥俱€佹爲銆佺煩闃电瓑鎶借薄銆佺粨鏋勫寲鐨勫舰寮忥紝杩欎笌娣卞害瀛︿範妯″瀷楂樼淮銆佸槇鏉備笖澶氬彉鐨勮緭鍏ュ緢涓嶅吋瀹癸紝鍥犳杩橀渶瑕佽缁冪紪鐮佸櫒f鍜岃В鐮佸櫒g锛屽皢鎶借薄褰㈠紡杞崲涓鸿嚜鐒跺舰寮忋€?
- ![](http://lib.ia.ac.cn:8003/ContentDelivery/20240619/06zc2.04_CDB708FC9A27BC289DDAB7A1F81FE99A.png)

NAR 娉涘寲鑳藉姏浼间箮杩滆繙浼樹簬Transformer鏋舵瀯

璇﹁: [鎷晳Transformer鎺ㄧ悊鑳藉姏锛丏eepMind鏂扮爺绌禩ransNAR锛氱粰妯″瀷宓屽叆銆岀畻娉曟帹鐞嗗ぇ鑴戙€峕(http://lib.ia.ac.cn/news/newsdetail/68837)

### 璁＄畻鏁堢巼

attention 瀛樺湪 $n^2$ 鐨勮绠楀鏉傚害锛屽浣曞疄鐜版洿闀挎枃鏈殑璁＄畻锛?
- 鍩轰簬鐘舵€佽凯浠?: TransformerXL RMT
- 鍩轰簬浣嶇疆缂栫爜澶栨帹鑳藉姏: ALiBi xPos Unlimiformer
- 鍩轰簬宸ョ▼浼樺寲: FlashAttention
- 鍩轰簬楂樻晥Attention: Reformer LinFormer Flash
- 鍏朵粬锛? S4, FLASH
- ![](https://pic3.zhimg.com/80/v2-fae510edc3aff2863cca31bc0dcd2046_1440w.webp)

#### 2023.6.14 FlashAttention

銆?2023-6-14銆慬FlashAttention: 鏇村揩璁粌鏇撮暱涓婁笅鏂囩殑GPT](https://www.bilibili.com/video/BV1SW4y1X7kh)
- 灏? transformer 鐨? qkv 璁＄畻鍔犻€燂紝鏂规硶锛氬悜閲忓垎鍧楀苟琛?
- 瑙嗛鏈夌壒鏁堛€?
- [椋炰功鍚堥泦鏂囨。](https://bytedance.feishu.cn/docx/doxcn3zm448MK9sK6pHuPsqtH8f)
- [FlashAttention](https://readpaper.feishu.cn/docx/AC7JdtLrhoKpgxxSRM8cfUounsh)
- [GitHub CodeRepo](https://github.com/cauyxy/bilivideos/tree/master/flash-attn)

<iframe src="//player.bilibili.com/player.html?aid=954566955&bvid=BV1SW4y1X7kh&cid=1158494106&page=1&autoplay=0" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"  height="600" width="100%" > </iframe>


#### 2023.6.24 PageAttention -- 绠＄悊qkv缂撳瓨

銆?2023-6-24銆慤C Berkeley 鍥㈤槦鎺ㄥ嚭涓€涓敤浜庡姞閫烲LM鎺ㄧ悊鐨勫紑婧愬簱`vLLM`锛孷icuna 鍦ㄧ嚎鎺ㄧ悊鏈嶅姟鐨勫箷鍚庤嫳闆勩€?
- 鍒╃敤 PagedAttention 鎶€鏈紝鏈夋晥绠＄悊Attention妯″潡涓殑Key鍜孷alue鐨凜ache锛岄噸鏂板畾涔変簡LLM鐨勬帹鐞嗘湇鍔°€?
- 鏃犻渶鏇存敼浠讳綍妯″瀷鏋舵瀯锛屽悶鍚愰噺姣斿師鐢? HF Transformers 楂樺嚭**24鍊?**銆?

KV Cache 鏍稿績鎬濇兂
- 缂撳瓨骞堕噸鐢ㄤ箣鍓嶈绠楄繃鐨凨ey鍜孷alue, 閬垮厤閲嶅璁＄畻銆?

鐜版湁 Cache 浠嶅瓨鍦ㄤ竴浜涢棶棰橈紝
- Large 澶э細瀵逛簬LLaMA-13B涓殑鍗曚釜搴忓垪锛屽畠鍗犵敤楂樿揪1.7GB鐨勫唴瀛樸€?
- Dynamic 鍔ㄦ€侊細澶у皬鍙栧喅浜庡簭鍒楅暱搴︼紝鑰屽簭鍒楅暱搴﹀叿鏈夐珮搴﹀彲鍙樺拰涓嶅彲棰勬祴鐨勭壒鐐广€?

鍥犳锛岄珮鏁堝湴绠＄悊 KV Cache 鏄噸澶ф寫鎴樸€?
- 鐜版湁绯荤粺锛圚uggingFace 榛樿瀹炵幇鏄痯ytorch鐨勫唴瀛樺垎閰嶇瓥鐣ワ級鐢变簬鍐呭瓨纰庣墖鍖栧拰杩囧害棰勭暀鑰屾氮璐逛簡60%-80%鐨勫唴瀛樸€?

涓轰簡瑙ｅ喅杩欎釜闂锛屽紩鍏ヤ簡 PagedAttention锛屼竴绉嶅彈浼犵粺鎿嶄綔绯荤粺**铏氭嫙鍐呭瓨**鍜?**鍒嗛〉**姒傚康鍚彂鐨勬敞鎰忓姏绠楁硶銆?
- 涓庝紶缁熸敞鎰忓姏绠楁硶涓嶅悓锛孭agedAttention 鍏佽灏?**杩炵画鐨勯敭鍜屽€煎瓨鍌ㄥ湪闈炶繛缁殑鍐呭瓨绌洪棿**涓€?

PagedAttention 灏嗘瘡涓簭鍒楃殑 KV 缂撳瓨鍒嗘垚澶氫釜鍧楋紝姣忎釜鍧楀寘鍚浐瀹氭暟閲忕殑鏍囪鐨勯敭鍜屽€笺€?
- 鍦ㄦ敞鎰忓姏璁＄畻杩囩▼涓紝PagedAttention Kernel楂樻晥鍦拌瘑鍒拰鑾峰彇杩欎簺鍧楋紝閲囩敤骞惰鐨勬柟寮忓姞閫熻绠椼€傦紙鍜孊yteTransformer鐨勬€濇兂鏈夌偣鍍忥級

[vLLM 鍘熺悊璇﹁В](https://mp.weixin.qq.com/s/FFcZ1c_a3Ua0vLIj3DGaCQ)


#### 2023.7.4 FasterTransfomer

銆?2023-7-4銆慬FasterTransfomer](https://github.com/NVIDIA/FasterTransformer) 鏄? NVIDIA 楂樺害浼樺寲鐨? Transformer 妯″瀷搴擄紝鍦ㄧ敓鎴愭椂杈惧埌 **2.5鍊?**鐨勯€熷害锛岃瑙? [Inference with FasterTransformer](https://github.com/THUDM/GLM-130B/blob/main/docs/inference-with-fastertransformer.md) 

#### MHA -> DCMHA

KAN

銆?2024-5-25銆慬ICML2024楂樺垎璁烘枃锛佸ぇ妯″瀷璁＄畻鏁堢巼鏆存定鑷?200%](https://mp.weixin.qq.com/s/8650CfLSSRUPfiYUTakkNQ)

KAN绐佺劧鐖嗙伀锛屾垚涓哄彲浠ユ浛浠LP鐨勪竴绉嶅叏鏂扮缁忕綉缁滄灦鏋勶紝200涓弬鏁伴《30涓囧弬鏁帮紱鑰屼笖锛孏PT-4o鐨勭敓鎴愰€熷害涔熸槸鎯婅壋浜嗕竴浼楀ぇ妯″瀷鐖卞ソ鑰呫€?

澶фā鍨嬬殑璁＄畻鏁堢巼寰堥噸瑕侊紝鎻愬崌澶фā鍨嬬殑tokens鐢熸垚閫熷害鏄緢鍏抽敭鐨勪竴鐜€?

鑰屾彁鍗囧ぇ妯″瀷鐨則okens鐢熸垚閫熷害锛岄櫎浜嗚姳閽卞崌绾PU澶栵紝鏇撮暱鏁堢殑鍋氭硶鏄敼鍠凾ransformer妯″瀷鏋舵瀯鐨勮绠楁晥鐜囥€?

褰╀簯绉戞妧 瀵筎ransformer璁＄畻鏈€鑰楁椂鐨勬牳蹇冪粍浠垛€斺€?**澶氬ご娉ㄦ剰鍔涙ā鍧?**锛圡HA锛変笅鎵嬶紝灏員ransformer璁＄畻鎬ц兘鎻愬崌浜嗘湁2鍊嶄箣楂樸€?
- 璁烘枃鏍囬锛歔Improving Transformers with Dynamically Composable Multi-Head Attention](https://arxiv.org/abs/2405.08553)
- 寮€婧愰」鐩湴鍧€锛歔DCFormer](https://github.com/Caiyun-AI/DCFormer)

Github涓婂凡寮€婧愯繖椤瑰伐浣滅殑浠ｇ爜銆佹ā鍨嬪拰璁粌鏁版嵁闆嗐€?

鎵胯浇Transformer璁＄畻閲忕殑鏍稿績妯″潡鏄?**澶氬ご娉ㄦ剰鍔?**锛圡HA锛夋ā鍧楋紝浣嶇疆锛坧osition=i锛変笂鐨勬瘡涓€涓?**娉ㄦ剰鍔涘ご**锛坅ttention head锛変細涓庡叏閮ㄤ綅缃笂鐨勬敞鎰忓姏澶磋绠楀嚭涓€涓敞鎰忓姏鍒嗗竷鐭╅樀銆?
- 杩欎釜杩囩▼涓紝浣嶇疆 i 涓婄殑鍚勪釜娉ㄦ剰鍔涘ご璁＄畻鍑烘潵鐨勬敞鎰忓姏鍒嗗竷鐭╅樀鏄浉浜掔嫭绔嬬殑銆?

杩欑澶氬ご鐙珛璁＄畻鐨勬満鍒朵細甯︽潵涓ゅぇ闂锛?
- 浣庣З鐡堕锛圠ow-rank Bottleneck锛夛細娉ㄦ剰鍔涚煩闃电殑绉╄緝浣庯紝妯″瀷鐨勮〃杈捐兘鍔涘彈闄?
- 澶村啑浣欙紙Head Redundancy锛夛細涓嶅悓鐨勬敞鎰忓姏澶村彲鑳戒細瀛︿範鍒扮浉浼肩殑妯″紡锛屽鑷村啑浣?

鍥犳锛屽僵浜戠鎶€鎻愬嚭浜嗕竴绉嶅彨**鍔ㄦ€佸彲缁勫悎**澶氬ご娉ㄦ剰鍔涳紙DCMHA锛夌殑鏈哄埗锛孌CMHA 閫氳繃涓€涓牳蹇冪殑缁勫悎鍑芥暟锛圕ompose function锛夛紝浠ヨ緭鍏ヤ緷璧栫殑鏂瑰紡杞崲娉ㄦ剰鍔涘緱鍒嗗拰鏉冮噸鐭╅樀锛屼粠鑰屽姩鎬佸湴缁勫悎娉ㄦ剰鍔涘ご锛岃В鍐充簡浼犵粺MHA妯″潡涓瓨鍦ㄧ殑涓婅堪浣庣З鐡堕鍜屽ご鍐椾綑闂銆?

DCMHA鏃ㄥ湪鎻愰珮妯″瀷鐨勮〃杈捐兘鍔涳紝鍚屾椂淇濇寔鍙傛暟鍜岃绠楁晥鐜囷紝鍙互浣滀负浠讳綍Transformer鏋舵瀯涓璏HA妯″潡鐨勫嵆鎻掑嵆鐢ㄦ浛浠ｅ搧锛屼互鑾峰緱鐩稿簲鐨凞CFormer妯″瀷銆?

DCMHA鏈哄埗鐨勬牳蹇冩槸寮曞叆鐨凜ompose鍑芥暟銆傝繖涓狢ompose鍑芥暟鍙互瑙嗕负涓€涓彲瀛︿範鐨勫弬鏁帮紝瀹冨彲浠ュ姩鎬佸湴缁勫悎涓嶅悓澶寸殑QK鐭╅樀鍜孷O鐭╅樀锛屽唴閮ㄩ€氳繃涓€绯诲垪鍙樻崲鏉ュ垎瑙ｅ拰閲嶆瀯娉ㄦ剰鍔涘悜閲忋€傚彲浠ヨ繎浼肩悊瑙ｄ负锛氱粡杩囩粍鍚堟槧灏勫悗锛孒涓熀纭€鐨勬敞鎰忓姏澶村彲缁勫悎鎴愬鑷矵*H涓敞鎰忓姏澶淬€?

鏍规嵁杈撳叆鏁版嵁璋冩暣澶翠箣闂寸殑浜や簰鏂瑰紡
- 涓€鏄墦鐮村ご鐨勭嫭绔嬫€?
- 浜屾槸鍙互鏍规嵁杈撳叆鏁版嵁鍔ㄦ€佺粍鍚?

浠庤€屽彲浠ュ寮烘ā鍨嬬殑琛ㄨ揪鑳藉姏銆?

鏁堟灉

璁烘枃閫氳繃瀹為獙琛ㄦ槑锛? `DCFormer` 鍦ㄤ笉鍚岀殑鏋舵瀯鍜屾ā鍨嬭妯′笅锛屽湪璇█寤烘ā鏂归潰鏄捐憲浼樹簬Transformer锛屼笌璁＄畻閲忓鍔?1.7鍊嶈嚦2鍊嶇殑妯″瀷鎬ц兘鐩稿尮閰嶃€?

DCFormer鍙彁楂?70%~100%鐨勬ā鍨嬭绠楁晥鐜?
- DCFormer 鍦ㄤ笉鍚屽弬鏁拌妯′笅锛?405M鍒?6.9B鍙傛暟锛夛紝瀵? Transformer 鍜? Transformer++ 妯″瀷鐨勬€ц兘鎻愬崌鏄捐憲
- DCPythia-6.9B 鍦ㄩ璁粌鍥版儜搴﹀拰涓嬫父浠诲姟璇勪及鏂归潰浼樹簬寮€婧愮殑Pythia-12B銆?
- ImageNet-1K鏁版嵁闆嗕笂鐨勫疄楠岄獙璇佷簡DCMHA鍦ㄩ潪璇█浠诲姟涓篃鏄湁鏁堟€х殑銆?

鐩稿悓鐨勫弬鏁伴噺涓嬶紝浣跨敤DCFormer灏嗗叿澶囨洿寮虹殑妯″瀷琛ㄨ揪鑳藉姏锛涚敤鏇村皯鐨勫弬鏁伴噺锛屾嫢鏈夌浉鍚岀殑妯″瀷琛ㄧず鏁堟灉銆?

DCFormer鍦ㄤ笉鍚岀殑鏋舵瀯鍜屾ā鍨嬭妯′笅锛屽湪璇█寤烘ā鏂归潰鏄捐憲浼樹簬Transformer锛屼笌璁＄畻閲忓鍔?1.7鍊嶈嚦2鍊嶇殑妯″瀷鎬ц兘鐩稿尮閰嶃€?


### 闀垮害闄愬埗

鏂囨湰闀垮害涓€鐩存槸 transformer 鐨勭‖浼ゃ€?
- 涓嶅悓浜? RNN锛宼ransformer 鍦ㄨ缁冩椂蹇呴』鍗″湪涓€涓?**鏈€澶ч暱搴?**涓婏紝杩欏皢瀵艰嚧璁粌濂界殑妯″瀷鏃犳硶鍦ㄤ竴涓笌璁粌鏃剁殑闀垮害鐩稿樊杈冭繙鐨勫彞瀛愪笂鍙栧緱杈冨ソ鐨勬帹鐞嗙粨鏋溿€?

Transformer 涓紝鐢变簬 token 鍜? token 涔嬮棿鏄病鏈夐『搴忎箣鍒嗙殑. 鍥犳锛岄€氬父鍦ㄨ緭鍏ユ坊鍔? Position Embedding 鏉ヨ〃寰佹瘡涓€涓? token 鍦ㄥ彞瀛愪腑鐨勪綅缃€?

Position Embedding 鐨勫浣曢€夋嫨瀹炲湪鏄竴涓毦棰橈紝閫氬父鏈変互涓嬪嚑绉嶏細
- 鍙涔犵殑鍙傛暟锛氳繖绉嶆瘮杈冨父瑙侊紝BRET 涓氨鏄繖涔堝仛鐨勶紝浣嗚繖绉嶆柟寮忓紛绔緢鏄庢樉锛屽洜涓轰綅缃俊鎭槸瀛︿範鍑烘潵鐨勶紝鎵€浠ュ鏋滆缁冮泦閲岄潰娌℃湁瑙佽繃瑕嗙洊鏌愪釜闀垮害锛屾帹鐞嗙殑鏁堟灉灏辨棤娉曞緱鍒颁繚璇併€?
- 姝ｅ鸡浣嶇疆缂栫爜锛氳繖鏄棭鏈? transformer 浣跨敤鐨勪綅缃紪鐮侊紝璁烘枃涓湁灏濊瘯鍋氬疄楠岋紝杩欑缂栫爜浼氶殢鐫€璁粌/棰勬祴鏃剁殑鏂囨湰闀垮害宸紓澧炲ぇ锛岋紙瓒呰繃 50 涓猼oken 鍚庯級鎬ц兘鏄捐憲涓嬮檷銆?
- 鏃嬭浆缂栫爜锛氳鏂囦腑鎻愬埌杩欑鏂瑰紡鏄瘮杈冧笉閿欑殑锛屽彧涓嶈繃鍥犲叾鍦ㄦ瘡涓€灞傞兘瑕佸仛涓€娆″悜閲忔棆杞紝浠庤€岄檷浣庤缁冨拰鎺ㄧ悊鐨勯€熷害銆?

transformer 杩欑被妯″瀷鐨? 鏃堕棿澶嶆潅搴︺€佸唴瀛樹娇鐢ㄥ鏉傚害閮芥槸 n^2锛坣涓哄簭鍒楅暱搴︼級
- 褰撳簭鍒楅暱搴﹁秴杩? 512 鏃讹紝妯″瀷瀵圭畻鍔涚殑瑕佹眰灏嗕細澶у箙鎻愰珮銆?

鏈€杩戜竴浜涙枃绔? Longformer, Performer, Reformer, Clustered attention 閮借瘯鍥鹃€氳繃杩戜技鍏ㄦ敞鎰忓姏鏈哄埗鏀瑰杽璇ラ棶棰樸€?

鍑咮ERT娉ㄦ剰鍔涙満鍒舵椂锛岄棶棰樺彲鑳芥湁锛?
- 姣忎釜璇嶄笌鍏朵粬鎵€鏈夎瘝閮芥湁鍏崇郴鍚楋紵
- 涓轰粈涔堟瘡涓瘝鐨勬敞鎰忓姏涓嶄粎浠呴泦涓湪鏈€閲嶈鐨勮瘝
- 濡備綍鐭ラ亾鍝簺璇嶆槸閲嶈鐨?
- 濡備綍鏈夋晥鐨勮娉ㄦ剰鍔涗粎鑰冭檻涓埆涓€浜涜瘝



#### 銆?2020-12-2銆慉llenAI Longformer

銆?2020-12-2銆慉llen AI 鎺ㄥ嚭 Longformer
- 浠嬬粛 [Longformer: Transformer 鏀硅繘鐗堬紝鍙鐞嗚緝闀跨殑搴忓垪](https://ai-scholar.tech/zh/articles/bert/longformer)
- 璁烘枃: [Longformer: The Long-Document Transformer](https://arxiv.org/pdf/2004.05150.pdf)
- huggingface [longformer](https://huggingface.co/docs/transformers/model_doc/longformer)

Transformer 璁＄畻澶嶆潅搴﹂殢杈撳叆搴忓垪鐨勫鍔犺€屽憟浜屾鏇茬嚎澧炲姞, 鏃堕棿鍜屽唴瀛樺崰鐢ㄩ潪甯稿ぇ
- 鍘熷洜锛歍ransformer 涓昏閮ㄥ垎 -- **缂╂斁鐐圭Н鑷敞鎰忓姏**锛圫caled Dot-Product Self-Attention锛?
- 鑷敞鎰忓姏鐨勮绠楀鏉傚害涓? `O(N^2)` 锛屽綋鍖呭惈闀垮彞鏃讹紝鍐呭瓨浣跨敤閲忎細闅忕潃杈撳叆閲忕殑澧炲姞鑰屽憟4鍊嶅闀裤€?

Longformer 鏄熀浜? Transformer 鐨勫彲鎵╁睍妯″瀷锛岀敤浜庡鐞?**闀挎枃妗?**锛屽彲杞绘澗鎵ц鍚勭鏂囨。绾? NLP 浠诲姟锛岃€屾棤闇€瀵归暱杈撳叆杩涜鍒嗗潡鎴栫缉鐭紝涔熸棤闇€浣跨敤澶嶆潅鐨勬灦鏋勬潵缁勫悎鍚勫潡淇℃伅銆?

Longformer 缁撳悎鏈湴鍜屽叏灞€淇℃伅锛屼互鍙婁笁绉嶆敞鎰忓姏锛堟粦鍔ㄧ獥鍙ｆ敞鎰忓姏銆佹斁澶ф粦鍔ㄧ獥鍙ｆ敞鎰忓姏鍜屽叏灞€娉ㄦ剰鍔涳級銆傜獥鍙ｆ敞鎰忓拰鍏ㄥ眬娉ㄦ剰锛夈€?
- ![](https://aisholar.s3.ap-northeast-1.amazonaws.com/media/August2023/%E3%82%B9%E3%82%AF%E3%83%AA%E3%83%BC%E3%83%B3%E3%82%B7%E3%83%A7%E3%83%83%E3%83%88_2023-08-05_7.16.49.png)

鏁堟灉
- Longformer 杩樺湪 text8 鍜? enwik8 浠诲姟涓彇寰椾簡鏈€浣虫€ц兘銆?
- Longformer 鍦ㄩ暱鏂囨。琛ㄧ幇涓€鐩翠紭浜? RoBERTa锛屽苟涓斿湪棰勮缁冨悗鐨? WikiHop 鍜? TriviaQA 浠诲姟涓〃鐜版渶浣炽€?

RoBERTa 鍙湁 512 涓綅缃祵鍏ワ紝鍥犳闇€瑕佸鍒? 8 涓綅缃祵鍏ユ潵瀹圭撼 4096 涓瓧銆傚敖绠″畠寰堢畝鍗曪紝浣嗘嵁绉板嵈闈炲父鏈夋晥锛岃繖鏄剧劧鏄洜涓哄鍒舵秷闄や簡鍒嗗尯杈圭晫銆?

#### 銆?2021-1-8銆戣胺姝? BigBird


銆?2021-1-8銆戣胺姝屾帹鍑? BigBird, 鍩轰簬**绋€鐤忔敞鎰忓姏**鐨凾ransformer锛屽皢鍩轰簬Transformer鐨勬ā鍨嬶紙渚嬪 BERT锛夋墿灞曞埌鏇撮暱鐨勫簭鍒椼€?
- 骞虫柟绾у埆鐨勪緷璧栭檷鎴愮嚎鎬?
- 鍚岀瓑纭欢鏉′欢涓嬶紝闀垮害鎵╁厖8鍊?
- 璁烘枃锛歔Big Bird: Transformers for Longer Sequences](https://arxiv.org/abs/2007.14062)
- 浠ｇ爜锛歔bigbird](https://github.com/google-research/bigbird)

寮€婧愪腑鏂? bigbird 棰勮缁冩ā鍨嬶紝浠巘iny鑷砨ase鍏?5涓骇鍒璁粌妯″瀷銆傚彲浠嶽huggingface hub](https://huggingface.co/models?language=zh&sort=downloads&search=bigbird)鐩存帴涓嬭浇浣跨敤

BigBird 妯″瀷瀹炵幇浜嗕笁绉嶆敞鎰忓姏鏈哄埗锛?**闅忔満娉ㄦ剰鍔?**銆?**绐楀彛娉ㄦ剰鍔?**鍜?**鍏ㄥ眬娉ㄦ剰鍔?**锛岃繖涓嶭ongFormer鍑犱箮鐩镐技

涓嶣ERT鍚岀瓑璁＄畻鍔涗笅锛屽彲澶勭悊搴忓垪闀垮害杈惧埌4096銆?
- 寰堝闀挎枃鏈簭鍒楃殑浠诲姟涓婅揪鍒癝OTA鏁堟灉锛屼緥濡傦細闀挎枃鏈憳瑕併€侀暱鏂囨湰闂瓟銆? 
- BigBird RoBERTa 妯″瀷鍦═ransformers浠撳簱涓娇鐢ㄣ€?

BigBird鐨勬敞鎰忓姏鏈哄埗鏄竴涓繎浼糂ERT鐨?**鍏ㄦ敞鎰忓姏鏈哄埗**锛屽洜姝や笉鏄瘮BERT鐨勬敞鎰忓姏鏈哄埗鏁堟灉鏇村ソ锛岃€屾槸**杩愯鏁堢巼鏇撮珮**銆?
- BERT鐨勬敞鎰忓姏鏈哄埗瀛樺偍涓庡簭鍒楅暱搴︽槸浜屾鏂瑰叧绯伙紝鍦ㄩ暱鏂囨湰鎯呭喌涓嬬殑瀛樺偍闇€姹傚氨宸茬粡寮€濮嬩护浜洪毦浠ュ繊鍙?
- 鑰? BigBird 鐨? block sparse attention 灏辨槸涓轰簡瑙ｅ喅杩欎釜闂銆傛棤闄愰暱闀垮害搴忓垪涓婏紝璁＄畻鏃犵┓娆? 娆℃椂锛屾妸BERT鐨勫叏娉ㄦ剰鍔涙満鍒舵崲鎴? block sparse attention銆? 


BigBird鏈変袱绉嶉暱绋嬫敞鎰忓姏鏂瑰紡锛屽彲浠ヨ璁＄畻鍙樼殑鏇存湁鏁堬細
- 鍏ㄥ眬璇嶏紙Global token锛夛細鏈変竴浜涜瘝锛岄渶瑕佽€冭檻鍏朵粬鎵€鏈夎瘝锛屽叾浠栨墍鏈夎瘝涔熼渶瑕佽€冭檻瀹冦€備緥濡傗€滺uggingFace is building nice libraries for easy NLP鈥溿€傚鏋溾€漛uilding鈥滄槸涓€涓叏灞€璇嶏紝妯″瀷鍦ㄦ湁鐨勪汉鐗╀腑闇€瑕佺煡閬撹瘝鈥漀LP鈥滃拰璇嶁€滺uggingFace鈥滅殑鍏崇郴锛堣繖涓や釜璇嶅湪鏈€宸﹁竟鍜屾渶鍙宠竟锛夛紝閭ｄ箞璇嶁€漛uilding鈥滈渶瑕佽璁剧疆鎴愬叏灞€璇嶏紝浠庤€屽鐞嗕笌鈥漀LP鈥滃拰鈥滺uggingFace鈥滅殑鍏崇郴銆?
- 闅忔満璇嶏紙Random tokens锛夛細闅忔満閫夋嫨涓€浜涜瘝锛屾妸淇℃伅浼犻€掔粰鍏朵粬璇嶏紝杩欏彲浠ラ檷浣庤瘝涓庤瘝涔嬮棿鐨勪俊鎭氦浜掗毦搴︺€?

```py
# 渚嬪绗竴涓瘝鍜屾渶鍚庝竴涓瘝鏄叏灞€鐨?
global_tokens = ["BigBird", "answering"]
# 灏嗗叏灞€璇嶅姞鍏ヨ嚦key_tokens闆嗗悎涓?
key_tokens.append(global_tokens)
# 鐜板湪鐢ㄨ瘝鈥漣s鈥滃仛闅忔満璇?
random_tokens = ["is"]
key_tokens.append(random_tokens)
key_tokens # {'now', 'is', 'in', 'answering', 'available', 'BigBird'}
# 鐜板湪锛岃瘝鈥漚vailable鈥滃彲浠ュ彧涓庤繖浜涜瘝鍋氭敞鎰忓姏璁＄畻锛岃€屼笉鏄墍鏈夎瘝
```

鍙傝€?
- [bigbird闀挎枃鏈璁粌妯″瀷浠嬬粛](https://zhuanlan.zhihu.com/p/444333724)
- [BigBird锛氬ぇ楦熸ā鍨嬩腑鏂囩敓鎴愬紡闀挎枃鏈憳瑕佸疄璺礭(https://blog.csdn.net/yjh_SE007/article/details/129244755)

#### 2022.*.* Attention with Linear Bias锛圓LiBi锛?

ALiBi 鏄? 2022 骞存彁鍑虹殑涓€绉嶆柟娉曪紝瑙ｅ喅 transformer **璁粌鍜屾帹鐞嗘椂鏂囨湰闀垮害涓嶄竴鑷?**鐨勯毦棰橈紝
- 璁烘枃涓湪璁粌鏃跺€欎娇鐢? 1024 鐨勬渶澶ч暱搴︼紝浣嗗湪鎺ㄧ悊鏃剁敤 2048 鐨勬渶澶ч暱搴︽帹鐞嗭紝骞朵笖鍦? PPL 鎸囨爣鎸佸钩銆?
- ALiBi 閮芥槸鍦ㄦ祴璇曢泦鐨勫彞瀛愭渶澶ч暱搴︾殑銆屼竴鍗婇暱搴︺€嶄笂杩涜璁粌锛岃€? Sinusoidal 鍒欐槸姝ｅ父鍦ㄣ€屾祴璇曢泦闀垮害銆嶄笂杩涜璁粌锛?
- [TRAIN SHORT, TEST LONG: ATTENTION WITH LINEAR BIASES ENABLES INPUT LENGTH EXTRAPOLATION](https://arxiv.org/pdf/2108.12409.pdf)

濡備綍瀹炵幇锛?
- ALiBi 瀹炵幇鎬濊矾寰堢洿瑙夛紝妯″瀷鍦ㄦ帴鏀惰緭鍏ユ椂鐩存帴鍘绘帀 Position Embedding 鍚戦噺锛岃€屾槸鍦? Attention 涓绠? query路Key 鐨勫€煎悗闈㈠姞鍏ヤ竴涓亸缃父閲忥紙闈炶缁冨彉閲忥級锛屾潵杈惧埌娉ㄥ叆浣嶇疆淇℃伅鐨勬晥鏋溿€傝繖涓父閲忔槸涓€涓? 浜嬪厛璁＄畻濂? 鐨勬暟鍊硷紝骞朵笖姣忎釜澶达紙head锛夌殑鍊奸兘鏈夋墍涓嶅悓銆?
- 閫氳繃銆岀浉瀵逛綅缃俊鎭€嶅氨鑳藉湪涓€瀹氱▼搴︿笂缂撹В銆岀粷瀵逛綅缃俊鎭€嶉€犳垚鐨勮缁冨拰鎺ㄧ悊杩囩▼涓暱搴︾紪鐮佷笉涓€鑷寸殑闂

浠ｇ爜瑙乕鍘熸枃](https://zhuanlan.zhihu.com/p/634236135)


#### 2024.4.10 Infini-Transformer

銆?2024-4-11銆慬Google 鎻愬嚭Infini-Transformer鏋舵瀯锛屽彲璁㎜LMs澶勭悊鏃犻檺闀夸笂涓嬫枃锛屽唴瀛樿妭绾?114鍊峕(https://mp.weixin.qq.com/s/factToEEJdWcs5WJG1Ljfg)
- [Leave No Context Behind: Efficient Infinite Context Transformers with Infini-attention](https://arxiv.org/pdf/2404.07143.pdf)

瀵逛簬鎵归噺澶у皬涓? 512銆佷笂涓嬫枃闀垮害涓? 2048 鐨? 500B 妯″瀷锛屾敞鎰忓姏閿€? (KV) 鐘舵€佺殑鍐呭瓨鍗犵敤涓? 3TB

闈㈠瓒呴暱搴忓垪锛岀浉姣旀敞鎰忓姏鏈哄埗锛屽唴瀛樺帇缂╂妧鏈洿鍏锋墿灞曟€с€?
- 鍐呭瓨鍘嬬缉涓嶄娇鐢ㄩ殢杈撳叆搴忓垪闀垮害鑰屽闀跨殑鏁扮粍锛岃€屾槸鍦ㄦ湁闄愮殑鍐呭瓨璧勬簮涓婏紝缁存姢鍥哄畾鏁伴噺鐨勫弬鏁版潵杩涜淇℃伅鐨勫瓨鍌ㄥ拰鍥炶皟銆?
- 鐒惰€岋紝鐩墠鐨凩LMs灏氭湭鏈変竴绉嶆湁鏁堛€佸疄鐢ㄧ殑鍐呭瓨鍘嬬缉鎶€鏈紝鍙互鍦ㄧ畝鍗曟€т笌璐ㄩ噺涔嬮棿鍙栧緱骞宠　銆?

鍩轰簬浠ヤ笂鑳屾櫙锛屼綔鑰呮彁鍑轰簡涓€绉嶆柊鏋舵瀯锛欼nfini-Transformer锛岃兘澶熻鍩轰簬Transformer鐨勫ぇ妯″瀷鍦ㄦ湁闄愬唴瀛樸€佽绠楄祫婧愮殑鏉′欢涓嬶紝澶勭悊鏃犻檺闀跨殑涓婁笅鏂囪緭鍏ャ€?

Infini-Transformer 鍙湪鏈夐檺鍐呭瓨鏉′欢涓嬶紝璁╁熀浜嶵ransformer鐨勫ぇ璇█妯″瀷锛圠LMs锛夐珮鏁堝鐞嗘棤闄愰暱鐨勮緭鍏ュ簭鍒椼€?

涓嶵ransformer-XL绫讳技锛孖nfini-Transformer澶勭悊鐨勬槸涓€绯诲垪鐗囨銆?
- 姣忎釜鐗囨鍐? 璁＄畻 standard causal 鐐圭Нattention context锛堟敞鎰忓姏涓婁笅鏂囷級銆傚洜姝わ紝鐐圭Н娉ㄦ剰鍔涜绠楀湪鏌愮鎰忎箟涓婃槸**灞€閮?**鐨勶紝瑕嗙洊浜嗙储寮曚负 S 鐨勫綋鍓嶇墖娈电殑鎬诲叡 N 涓爣璁般€?
- 鐒惰€岋紝灞€閮ㄦ敞鎰忓姏鍦ㄥ鐞嗕笅涓€涓墖娈垫椂浼氫涪寮冨墠涓€涓墖娈电殑娉ㄦ剰鍔涚姸鎬併€傚湪Infini-Transformer涓紝骞舵病鏈夊拷鐣ユ棫鐨勯敭鍊硷紙KV锛夋敞鎰忓姏鐘舵€侊紝鑰屾槸閫氳繃鍐呭瓨鍘嬬缉鎶€鏈噸鏂颁娇鐢ㄥ畠浠潵淇濇寔鏁翠釜涓婁笅鏂囧巻鍙层€?
- 鍥犳锛孖nfini-Transformer鐨勬瘡涓敞鎰忓姏灞傞兘鍏锋湁**鍏ㄥ眬**鍘嬬缉鍜?**灞€閮?**缁嗙矑搴︾姸鎬侊紝杩欏氨鏄墠闈㈡彁鍒扮殑鏃犻檺娉ㄦ剰鍔涳紙Infini-attention锛夈€?

瀹為獙缁撴灉琛ㄦ槑锛?
- Infini-Transformer鍦ㄩ暱涓婁笅鏂囪瑷€寤烘ā浠诲姟涓婅秴瓒婁簡鍩虹嚎妯″瀷锛屽唴瀛樻渶楂樺彲鑺傜害114鍊嶃€?



### TTT

銆?2024-7-20銆慬褰诲簳鏀瑰彉璇█妯″瀷锛氬叏鏂版灦鏋凾TT瓒呰秺Transformer锛孧L妯″瀷浠ｆ浛RNN闅愯棌鐘舵€乚(https://www.jiqizhixin.com/articles/2024-07-10-2)

闂
- 闀夸笂涓嬫枃鐨勬寫鎴樻槸 RNN 灞傛湰璐ㄤ笂鎵€鍥烘湁鐨勶細涓庤嚜娉ㄦ剰鍔涙満鍒朵笉鍚岋紝RNN 灞傚繀椤诲皢涓婁笅鏂囧帇缂╀负鍥哄畾澶у皬鐨勯殣钘忕姸鎬侊紝鏇存柊瑙勫垯闇€瑕佸彂鐜版暟鍗冪敋鑷虫暟鐧句竾涓? token 涔嬮棿鐨勫簳灞傜粨鏋勫拰鍏崇郴銆?

鏂潶绂忓ぇ瀛︺€佸姞宸炲ぇ瀛︿集鍏嬪埄鍒嗘牎銆佸姞宸炲ぇ瀛﹀湥杩垐鍒嗘牎鍜? Meta 璁捐浜嗕竴绉嶆柊鏋舵瀯 TTT锛岀敤**鏈哄櫒瀛︿範妯″瀷**鍙栦唬浜? **RNN 闅愯棌鐘舵€?**銆?
- 璇ユā鍨嬮€氳繃杈撳叆 token 鐨勫疄闄呮搴︿笅闄嶆潵鍘嬬缉涓婁笅鏂囥€?
- 娴嬭瘯鏃惰缁冿紙Test-Time Training锛?
- TTT 灞傜洿鎺ュ彇浠? Attention锛屽苟閫氳繃琛ㄨ揪鎬ц蹇嗚В閿佺嚎鎬у鏉傛€ф灦鏋勶紝浣挎垜浠兘澶熷湪涓婁笅鏂囦腑璁粌鍏锋湁鏁扮櫨涓囷紙鏈夋椂鏄暟鍗佷嚎锛変釜 token 鐨? LLM銆? 

TTT 灞備綔涓轰竴绉嶆柊鐨勪俊鎭帇缂╁拰妯″瀷璁板繂鏈哄埗锛屽彲绠€鍗曞湴鐩存帴鏇夸唬 Transformer 涓殑鑷敞鎰忓姏灞傘€?
- 涓? Mamba 鐩告瘮锛孴TT-Linear 鐨勫洶鎯戝害鏇翠綆锛孎LOP 鏇村皯锛堝乏锛夛紝瀵归暱涓婁笅鏂囩殑鍒╃敤鏇村ソ锛堝彸锛夛細

鍏ㄦ柊鐨勫ぇ璇█妯″瀷锛圠LM锛夋灦鏋勬湁鏈涗唬鏇胯嚦浠婂湪 AI 棰嗗煙濡傛棩涓ぉ鐨? Transformer锛屾€ц兘涔熸瘮 Mamba 鏇村ソ銆?
- 璁烘枃锛歔Learning to (Learn at Test Time): RNNs with Expressive Hidden States](https://arxiv.org/abs/2407.04620)
- 浠ｇ爜涓? jax 璁粌鍜屾祴璇曪細[ttt-lm-jax](https://github.com/test-time-training/ttt-lm-jax)
- PyTorch 鎺ㄧ悊浠ｇ爜锛歔ttt-lm-pytorch](https://github.com/test-time-training/ttt-lm-pytorch)

## 绋€鐤廇ttention

### 璧峰洜

transformer鑳芥崟鎹夎緭鍏ュ簭鍒梩oken涔嬮棿鐨勫叧绯伙紝鍗充娇鏄暱璺濈銆?

闀垮簭鍒楄緭鍏ュ彈鍒版敞鎰忓姏璁＄畻鍜屽唴瀛樿祫婧愰檺鍒讹紝闅忕潃搴忓垪闀垮害n浜屾澧為暱銆?
- DeepSpeed鎻愪緵浜? **绋€鐤? attention kernel** 鈥斺€? 鏀寔**闀垮簭鍒?**妯″瀷杈撳叆锛屽寘鎷枃鏈緭鍏ワ紝鍥惧儚杈撳叆鍜岃闊宠緭鍏ャ€?
- 閫氳繃鍧楃█鐤忚绠楀皢娉ㄦ剰鍔涚殑璁＄畻鍜屽唴瀛橀渶姹傞檷浣庡嚑涓暟閲忕骇銆?

璇ユ柟娉曚笉浠呯紦瑙ｄ簡娉ㄦ剰鍔涜绠楃殑鍐呭瓨鐡堕锛岃€屼笖鍙互鏈夋晥鍦版墽琛岀█鐤忚绠椼€?

闄や簡鎻愪緵骞挎硾鐨勭█鐤忔€х粨鏋勫锛岃繕鍏锋湁澶勭悊浠讳綍鐢ㄦ埛瀹氫箟鐨勫潡绋€鐤忕粨鏋勭殑鐏垫椿鎬с€?

### 鎬荤粨

绋€鐤廇ttention
- `Atrous Self Attention` 绌烘礊鑷敞鎰忓姏锛屽彧璁＄畻绗琸,2k,3k,4k...鍏冪礌
- `Local Self Attention`
- `Sparse Self Attention`: OpenAI鍦╥mage transformer涓紩鍏ヤ簡Sparse self-attention锛屾妸涓よ€呯粨鍚堝湪涓€鍧楋紝鏃㈠彲浠ュ涔犲埌灞€閮ㄧ殑鐗规€э紝鍙堝彲浠ュ涔犲埌杩滅▼绋€鐤忕殑鐩稿叧鎬?

|绋€鐤廇ttention|鍚嶇О|璇存槑||
|---|---|---|---|
|`Atrous Self Attention`|绌烘礊鑷敞鎰忓姏|![](https://pic2.zhimg.com/80/v2-a39db55945b1ae7c413572b22fbe4cd1_1440w.webp)||
|`Local Self Attention`|灞€閮ㄨ嚜娉ㄦ剰鍔泑![](https://pic4.zhimg.com/80/v2-c2b46a79fb998e2030ecd8cea99100fb_1440w.webp)||
|`Sparse Self Attention`|绋€鐤忚嚜娉ㄦ剰鍔泑![](https://pic4.zhimg.com/80/v2-a2f4cfa836abe8a6fc537048be262ab3_1440w.webp)|缁煎悎浠ヤ笂浼樼偣|

銆?2019-7-27銆戣嫃鍓戞灄锛孾鑺傜害鑰岀敓锛氫粠鏍囧噯Attention鍒扮█鐤廇ttention](https://spaces.ac.cn/archives/6853) 鑺傜害鏃堕棿銆佹樉瀛樸€?

Attention鐨勬牳蹇冨湪浜嶲,K,V 涓変釜鍚戦噺搴忓垪鐨勪氦浜掑拰铻嶅悎锛屽叾涓璔,K 鐨勪氦浜掔粰鍑轰簡涓や袱鍚戦噺涔嬮棿鐨勬煇绉嶇浉鍏冲害锛堟潈閲嶏級锛岃€屾渶鍚庣殑杈撳嚭搴忓垪鍒欐槸鎶奦鎸夌収鏉冮噸姹傚拰寰楀埌鐨?

鐞嗚涓婏紝Self Attention **璁＄畻鏃堕棿**鍜?**鏄惧瓨鍗犵敤閲?**閮芥槸 ?(n^2) 绾у埆鐨勶紙n鏄簭鍒楅暱搴︼級
- 濡傛灉搴忓垪闀垮害鍙樻垚鍘熸潵鐨?**2鍊?**锛屾樉瀛樺崰鐢ㄩ噺灏辨槸鍘熸潵鐨?**4鍊?**锛岃绠楁椂闂翠篃鏄師鏉ョ殑**4鍊?**銆?
- 褰撶劧锛屽亣璁惧苟琛屾牳蹇冩暟瓒冲澶氱殑鎯呭喌涓嬶紝璁＄畻鏃堕棿鏈繀浼氬鍔犲埌鍘熸潵鐨?4鍊嶏紝浣嗘槸鏄惧瓨鐨?4鍊嶅嵈鏄疄瀹炲湪鍦ㄧ殑锛屾棤鍙伩鍏嶏紝杩欎篃鏄井璋傿ert鏃禣OM鐨勫師鍥犮€?

涓轰粈涔堟槸 ?(n^2)锛?
- 瑕佸搴忓垪涓殑浠绘剰涓や釜鍚戦噺閮借璁＄畻鐩稿叧搴︼紝寰楀埌涓€涓?$n^2$澶у皬鐨勭浉鍏冲害鐭╅樀
- ![](https://spaces.ac.cn/usr/uploads/2019/07/775103900.png)
- 宸﹁竟鏄剧ず浜?**娉ㄦ剰鍔涚煩闃?**锛屽彸鍙樻樉绀轰簡**鍏宠仈鎬?**锛岃繖琛ㄦ槑姣忎釜鍏冪礌閮借窡搴忓垪鍐呮墍鏈夊厓绱犳湁鍏宠仈銆?

鎵€浠ワ紝鑺傜渷鏄惧瓨锛屽姞蹇绠楅€熷害锛屼竴涓В娉曟槸**鍑忓皯鍏宠仈鎬ц绠?**
- 姣忎釜鍏冪礌鍙窡搴忓垪鍐呯殑**閮ㄥ垎鍏冪礌**鐩稿叧锛岃繖灏辨槸绋€鐤廇ttention鐨勫熀鏈師鐞嗐€?
- 婧愪簬OpenAI鐨勮鏂囥€奫Generating Long Sequences with Sparse Transformers](https://arxiv.org/abs/1904.10509)銆?


### Atrous Self Attention 鑶ㄨ儉娉ㄦ剰鍔?

Atrous Self Attention锛屸€?**鑶ㄨ儉**鑷敞鎰忓姏鈥濄€佲€?**绌烘礊**鑷敞鎰忓姏鈥濄€佲€?**甯﹀瓟**鑷敞鎰忓姏鈥濈瓑銆?
- 鍚嶇О鏄嚜瀹氫箟, 鍘熻鏂囥€奊enerating Long Sequences with Sparse Transformers銆嬫病鏈夊嚭鐜拌繃杩欎袱涓蹇?

Atrous Self Attention 鍚彂浜庘€?**鑶ㄨ儉鍗风Н**锛圓trous Convolution锛夆€濓紝濡備笅鍥炬墍绀猴紝瀹冨鐩稿叧鎬ц繘琛屼簡绾︽潫锛屽己琛岃姹傛瘡涓厓绱犲彧璺熷畠鐩稿璺濈涓簁,2k,3k,鈥? 鐨勫厓绱犲叧鑱旓紝鍏朵腑k>1鏄鍏堣瀹氱殑瓒呭弬鏁般€備粠涓嬪乏鐨勬敞鎰忓姏鐭╅樀鐪嬶紝灏辨槸寮鸿瑕佹眰鐩稿璺濈涓嶆槸k
鐨勫€嶆暟鐨勬敞鎰忓姏涓?0锛堢櫧鑹蹭唬琛?0锛夛細
- ![](https://spaces.ac.cn/usr/uploads/2019/07/4107095412.png)
- Atrous Self Attention鐨勬敞鎰忓姏鐭╅樀锛堝乏锛夊拰鍏宠仈鍥剧ず锛堝彸锛?

鐢变簬鐜板湪璁＄畻娉ㄦ剰鍔涙槸鈥滆烦鐫€鈥濇潵浜嗭紝鎵€浠ュ疄闄呬笂姣忎釜鍏冪礌鍙窡澶х害n/k涓厓绱犵畻鐩稿叧鎬э紝杩欐牱鐞嗘兂鎯呭喌涓嬭繍琛屾晥鐜囧拰鏄惧瓨鍗犵敤閮藉彉鎴愪簡?(n^2/k)锛屼篃灏辨槸璇磋兘鐩存帴闄嶄綆鍒板師鏉ョ殑1/k銆?


### Local Self Attention 灞€閮ㄨ嚜娉ㄦ剰鍔?

Local Self Attention锛屼腑鏂囩О鈥滃眬閮ㄨ嚜娉ㄦ剰鍔涒€濄€?
- **鑷敞鎰忓姏**鏈哄埗鍦–V棰嗗煙缁熺О涓衡€淣on Local鈥?
- 鑰孡ocal Self Attention鍒欒鏀惧純鍏ㄥ眬鍏宠仈锛岄噸鏂板紩鍏?**灞€閮ㄥ叧鑱?**銆傜害鏉熸瘡涓厓绱犲彧涓庡墠鍚巏涓厓绱犱互鍙婅嚜韬湁鍏宠仈锛屽涓嬪浘鎵€绀猴細
- ![](https://spaces.ac.cn/usr/uploads/2019/07/713126535.png)
- Local Self Attention鐨勬敞鎰忓姏鐭╅樀锛堝乏锛夊拰鍏宠仈鍥剧ず锛堝彸锛?
- 浠庢敞鎰忓姏鐭╅樀鏉ョ湅锛屽氨鏄浉瀵硅窛绂昏秴杩噆鐨勬敞鎰忓姏閮界洿鎺ヨ涓?0銆?

鍏跺疄 Local Self Attention 璺熸櫘閫氬嵎绉緢鍍忎簡锛岄兘鏄繚鐣欎簡涓€涓? 2k+1 澶у皬鐨勭獥鍙ｏ紝鐒跺悗鍦ㄧ獥鍙ｅ唴杩涜涓€浜涜繍绠楋紝涓嶅悓鐨勬槸鏅€氬嵎绉槸鎶婄獥鍙ｅ睍骞崇劧鍚庢帴涓€涓叏杩炴帴灞傚緱鍒拌緭鍑猴紝鑰岀幇鍦ㄦ槸绐楀彛鍐呴€氳繃娉ㄦ剰鍔涙潵鍔犳潈骞冲潎寰楀埌杈撳嚭銆傚浜嶭ocal Self Attention鏉ヨ锛屾瘡涓厓绱犲彧璺? 2k+1 涓厓绱犵畻鐩稿叧鎬э紝杩欐牱涓€鏉ョ悊鎯虫儏鍐典笅杩愯鏁堢巼鍜屾樉瀛樺崰鐢ㄩ兘鍙樻垚浜? ?((2k+1)n)??(kn) 浜嗭紝涔熷氨鏄闅忕潃n 鑰岀嚎鎬у闀匡紝杩欐槸涓€涓緢鐞嗘兂鐨勬€ц川鈥斺€斿綋鐒朵篃鐩存帴鐗虹壊浜嗛暱绋嬪叧鑱旀€с€?

### Sparse Self Attention -- OpenAI鏀硅繘锛岀患鍚堜互涓婁袱绉?

鐜板湪鍙互寰堣嚜鐒跺湴寮曞叆OpenAI鐨? Sparse Self Attention浜嗐€?
- Atrous Self Attention 鏈変竴浜涙礊锛岃€? Local Self Attention姝ｅソ濉ˉ浜嗚繖浜涙礊锛屾墍浠ヤ竴涓畝鍗曟柟寮忓氨鏄皢Local Self Attention鍜孉trous Self Attention 浜ゆ浛浣跨敤锛屼袱鑰呯疮绉捣鏉ワ紝鐞嗚涓婁篃鍙互瀛︿範鍒板叏灞€鍏宠仈鎬э紝涔熺渷浜嗘樉瀛樸€?
- 鎬濊矾锛氱涓€灞傜敤Local Self Attention锛岃緭鍑虹殑姣忎釜鍚戦噺閮借瀺鍚堜簡灞€閮ㄥ嚑涓緭鍏ュ悜閲忥紝鐒跺悗绗簩灞傜敤Atrous Self Attention锛岃櫧鐒惰烦鐫€鏉ワ紝浣嗘槸鍥犱负绗竴灞傜殑杈撳嚭铻嶅悎浜嗗眬閮ㄧ殑杈撳叆鍚戦噺锛屾墍浠ョ浜屽眰鐨勮緭鍑虹悊璁轰笂鍙互璺熶换鎰忕殑杈撳叆鍚戦噺鐩稿叧锛屼篃灏辨槸璇村疄鐜颁簡**闀跨▼鍏宠仈**銆?
- 浣嗘槸OpenAI鐩存帴灏嗕袱涓狝trous Self Attention鍜孡ocal Self Attention鍚堝苟涓轰竴涓紝濡備笅鍥撅細
- ![](https://spaces.ac.cn/usr/uploads/2019/07/1199615308.png)
- Sparse Self Attention鐨勬敞鎰忓姏鐭╅樀锛堝乏锛夊拰鍏宠仈鍥剧ず锛堝彸锛?

浠庢敞鎰忓姏鐭╅樀涓婄湅灏卞緢瀹规槗鐞嗚В浜嗭紝灏辨槸闄や簡鐩稿璺濈涓嶈秴杩噆鐨勩€佺浉瀵硅窛绂讳负k,2k,3k,鈥? 鐨勬敞鎰忓姏閮借涓?0锛岃繖鏍蜂竴鏉ttention灏卞叿鏈夆€滃眬閮ㄧ揣瀵嗙浉鍏冲拰杩滅▼绋€鐤忕浉鍏斥€濈殑鐗规€э紝杩欏寰堝浠诲姟鏉ヨ鍙兘鏄竴涓笉閿欑殑鍏堥獙锛屽洜涓虹湡姝ｉ渶瑕佸瘑闆嗙殑闀跨▼鍏宠仈鐨勪换鍔′簨瀹炰笂鏄緢灏戠殑銆?

OpenAI 寮€婧愪簡瀹樻柟瀹炵幇 [sparse_attention](https://github.com/openai/sparse_attention)

## Transformer-Decoder

銆?2021-4-19銆慬https://zhuanlan.zhihu.com/p/179959751](https://zhuanlan.zhihu.com/p/79714797)

Transformer 鍘熷璁烘枃鍙戣〃涔嬪悗锛屻€孏enerating Wikipedia by Summarizing Long Sequences銆嶆彁鍑虹敤鍙︿竴绉? transformer 妯″潡鐨?**鎺掑垪鏂瑰紡**鏉ヨ繘琛岃瑷€寤烘ā
- 鐩存帴鎵旀帀浜嗘墍鏈夌殑 transformer 缂栫爜鍣ㄦā鍧椻€︹€︺€孴ransformer-Decoder銆嶆ā鍨嬨€?

鏃╂湡鐨勫熀浜? transformer 鐨勬ā鍨嬬敱 6 涓? transformer 瑙ｇ爜鍣ㄦā鍧楀爢鍙犺€屾垚锛?
- ![](https://pic3.zhimg.com/80/v2-19720b1c70a294558dc9456477156b06_1440w.webp)

瑙ｇ爜鍣ㄦā鍧?
- 鍜? transformer 鍘熷瑙ｇ爜鍣ㄦā鍧楃浉姣旓紝鍘绘帀浜嗙浜屼釜鑷敞鎰忓姏灞傘€?

涓€涓浉浼肩殑鏋舵瀯鍦?**瀛楃**绾у埆鐨勮瑷€寤烘ā涓篃琚獙璇佹湁鏁堬紝浣跨敤鏇存繁鐨勮嚜娉ㄦ剰鍔涘眰鏋勫缓璇█妯″瀷锛屼竴娆￠娴嬩竴涓瓧姣?/瀛楃銆?

鎵€鏈夎В鐮佸櫒妯″潡閮戒竴鏍枫€備娇鐢ㄥ甫鎺╂ā鐨勮嚜娉ㄦ剰鍔涘眰銆?
- 璇ユā鍨嬪湪鏌愪釜鐗囨涓彲浠ユ敮鎸佹渶闀? **4000** 涓崟璇嶇殑搴忓垪锛岀浉杈冧簬 transformer 鍘熷璁烘枃涓渶闀? **512** 鍗曡瘝鐨勯檺鍒舵湁浜嗗緢澶х殑鎻愬崌銆?


# 缁撴潫