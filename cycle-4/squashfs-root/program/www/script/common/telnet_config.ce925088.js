Config.telnet_config=function(n){var e={},i={},t={},a={friendPasswordEnable:["FriendlyPassword","Enabled"],MacAddressTest:["MacBind","Enabled"]};return new(Class.extend({init:function(){Utils.beforeDataLoad(),Utils.initLang(),this.initEvent(),this.initData(),Utils.afterDataLoad()},initData:function(){Utils.LAPI_GetCfgData(LAPI_URL.FriendPwd,i)?(Utils.LAPI_CfgToForm("frmSetupTelnet",i,e,a),t=Utils.objectClone(i),VersionType.IN==Capinfo.versionType&&n("#FriendPwdEnableDiv").addClass("hidden")):Utils.disableAll()},initEvent:function(){var e=this;n(".button_green").bind("click",function(){e.submitF()})},submitF:function(){!n("#friendPassword_close").prop("checked")||0!=Utils.checkStrong(Frame.loginUserPwd)&&1!=Utils.checkStrong(Frame.loginUserPwd)?(Utils.LAPI_FormToCfg("frmSetupTelnet",i,e,a),!Utils.isObjectEquals(i,t)?Utils.LAPI_SetCfgData(LAPI_URL.FriendPwd,i)&&(t=Utils.objectClone(i),Frame.isFriendPasswordEnable=e.friendPasswordEnable):parent.status=n.lang.tip.tipAnyChangeInfo):confirm(n.lang.tip.tipFriendlyStatus)?Frame.modifyPwd():(n("#friendPassword_enable").prop("checked",!0),n("#friendPassword_close").removeProp("checked"))},release:function(){delete Config.telnet_config}}))}(jQuery),Frame.currentNameSpace=Config.telnet_config;