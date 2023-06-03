Config.ManageServer=function(u){var o=!1,h={},d={},A=null,m=!1,C="0000000000000000",n={},s={},c={},v={},p={VMProtocol:["MngProtocol"],DeviceID:["DeviceID"],ServerID:["ServerID"],DeviceName:["DeviceName"],VMIPAddr:["Address"],VMPort:["Port"],VideoChlID:["VideoChlID"],AudioChlID:["AudioChlID"],ExpireTime:["Expire"]},P={IsUploadEnable:["Enable"],BMIPAddr:["ServerAddr"]},I={},S={},f={OnvifStorEnable:["Enable"],OnvifStorIpAddr:["StreamIPAddr"]};return new(Class.extend({init:function(){Utils.beforeDataLoad(),this.initPage(),Utils.initLang(),this.initValidator(),this.initEvent(),this.initData(),Utils.afterDataLoad()},initPage:function(){Capinfo.isSupportBMServer&&(u("#recordBackupTR").removeClass("hidden"),u("#bmAddrTR").removeClass("hidden")),this.initVMProtocol(),Capinfo.isSupportBMNoRebootPrompt||(u("#notice").removeClass("hidden"),u("#noticeHR").removeClass("hidden")),Capinfo.isSupportStorage&&u("#onvifStorDiv").removeClass("hidden"),Capinfo.isSupportNoBrand&&u("#VMProtocol_pub option[value=0]").text(u.lang.pub.privateProtocol)},initData:function(){n={},c={},Utils.LAPI_GetCfgData(LAPI_URL.DisconnectCache,I)?(S=Utils.objectClone(I),Utils.LAPI_CfgToForm("frmSetup",I,h,f),Utils.LAPI_GetCfgData(LAPI_URL.LAPI_ManageServer,n)&&Utils.LAPI_GetCfgData(LAPI_URL.LAPI_BMServer,c)?(s=Utils.objectClone(n),Utils.LAPI_CfgToForm("frmSetup",n,h,p),v=Utils.objectClone(c),Utils.LAPI_CfgToForm("frmSetup",c,h,P),2<h.VMProtocol?(h.VMProtocol_pub=3,h.VMProtocol_private=h.VMProtocol):(h.VMProtocol_pub=h.VMProtocol,h.VMProtocol_private=3),d=Utils.objectClone(h),Utils.cfgToForm(h,"frmSetup"),u("#VMPassword").val(C),this.VMprotocol_change(),Capinfo.isSupportBMServer&&this.BMAddressEnable(),this.OnvifAddressEnable()):Utils.disableAll()):Utils.disableAll()},initEvent:function(){var a=this;u("#VMProtocol_pub").change(function(){var e=u("#VMProtocol"),t=u("#VMPort");e.val(u("#VMProtocol_pub").val()),a.VMprotocol_change();e=Number(e.val());0==e?5063==parseInt(t.val())&&t.val(5060):1==e&&5060==parseInt(t.val())&&t.val(5063)}),u("#VMProtocol_private").change(function(){u("#VMProtocol").val(u("#VMProtocol_private").val()),a.VMprotocol_change()}),u("#VMIPAddr").change(function(){var e=u("#VMIPAddr");""==e.val()&&e.val("0.0.0.0")}),u("#BMIPAddr").change(function(){var e=u("#BMIPAddr");""==e.val()&&e.val("0.0.0.0")}),u("#OnvifStorIpAddr").change(function(){var e=u("#OnvifStorIpAddr");""==e.val()&&e.val("0.0.0.0")})},submitF:function(){var e=!1,t=u("#VMIPAddr"),a=u("#BMIPAddr");if(A.form()){if(!Capinfo.isSupportBMNoRebootPrompt&&(u("#DeviceID").val()!=h.DeviceID||t.val()!=h.VMIPAddr||u("#VMProtocol").val()!=h.VMProtocol)){var r=u.lang.tip.tipCfmChangeSysCfg;if(!confirm(r))return;o=!0}Utils.LAPI_FormToCfg("frmSetup",n,h,p);var i=!Utils.isObjectEquals(n,s);Utils.LAPI_FormToCfg("frmSetup",c,h,P);var l=!Utils.isObjectEquals(c,v),r=!Utils.isObjectEquals(h,d);if(r||m||i||l){if(""==t.val()&&t.val("0.0.0.0"),""==a.val()&&a.val("0.0.0.0"),m&&(n.RSAPublicKey={},n.RSAPublicKey.RSAPublicKeyE=Frame.RSAPublicKeyE,n.RSAPublicKey.RSAPublicKeyN=Frame.RSAPublicKeyN,n.RegPassword=Utils.encrypting(u("#VMPassword").val(),Frame.RSAKey)),Capinfo.isSupportBMServer&&l){if(!(e=Utils.LAPI_SetCfgData(LAPI_URL.LAPI_BMServer,c)))return;v=Utils.objectClone(c)}r&&(Utils.LAPI_FormToCfg("frmSetup",I,h,f),!Utils.isObjectEquals(I,S)&&(e=Utils.LAPI_SetCfgData(LAPI_URL.DisconnectCache,I))&&(S=Utils.objectClone(I))),Capinfo.isSupportVM?(i||m)&&Utils.LAPI_SetCfgData(LAPI_URL.LAPI_ManageServer,n,!1,this.callback):e&&o&&Utils.disableAll()}else Frame.showMsg(!0,u.lang.tip.tipAnyChangeInfo,0)}},callback:function(e){ResultCode.RESULT_CODE_SUCCEED==e?(m&&(delete n.RSAPublicKey,delete n.RegPassword),s=Utils.objectClone(n),m=!1,u("#VMPassword").val(C),Frame.showMsg(!0),o&&Utils.disableAll()):ResultCode.RESULT_RASPUBLICKEY_AUTH_ERR==e?(e={},Utils.LAPI_GetCfgData(LAPI_URL.SecurityRSA,e)&&(setMaxDigits(130),Frame.RSAPublicKeyE=e.RSAPublicKeyE,Frame.RSAPublicKeyN=e.RSAPublicKeyN,Frame.RSAKey=new RSAKeyPair(Frame.RSAPublicKeyE,"",Frame.RSAPublicKeyN),n.RSAPublicKey={},n.RSAPublicKey.RSAPublicKeyE=Frame.RSAPublicKeyE,n.RSAPublicKey.RSAPublicKeyN=Frame.RSAPublicKeyN,n.RegPassword=Utils.encrypting(u("#VMPassword").val(),Frame.RSAKey),Utils.LAPI_SetCfgData(LAPI_URL.LAPI_ManageServer,n,!1,Config.ManageServer.callback))):Frame.showMsg(!1,u.lang.tip.tipSetCfgFail)},release:function(){Frame.currentNameSpace="",delete Config.ManageServer},initValidator:function(){u("#DeviceID").attr("tip",u.lang.tip.tipDeviceID),u("#VideoChlID").attr("tip",u.lang.tip.tipPassword),u("#AudioChlID").attr("tip",u.lang.tip.tipPassword),u("#DeviceName").attr("tip",u.lang.tip.tipDeviceName),u("#ServerID").attr("tip",u.lang.tip.tipDeviceID),u("#VMIPAddr").attr("tip",u.lang.tip.tipGatewayInfo),u("#VMPort").attr("tip",u.validator.format(u.lang.tip.tipIntRange,1025,65535)),u("#VMPassword").attr("tip",u.lang.tip.tipVMPwd),u("#BMIPAddr").attr("tip",u.lang.tip.tipGatewayInfo),u("#OnvifStorIpAddr").attr("tip",u.lang.tip.tipGatewayInfo),u("#ExpireTime").attr("tip",u.validator.format(u.lang.tip.tipIntRange,3600,36e3)),u.validator.addMethod("isIPAddress",function(e){return Utils.isIPAddress(e)},u.lang.tip.tipIPErr),u.validator.addMethod("checkIP1To223",function(e){return Utils.checkIP1To223(e)},u.lang.tip.tipIPRangeErr),u.validator.addMethod("checkIPAddrOrEmpty",function(e){return Utils.checkIPAddrOrEmpty(e)},u.lang.tip.tipIPErr),u.validator.addMethod("checkIP1To223OrEmpty",function(e){return Utils.checkIP1To223OrEmpty(e)},u.lang.tip.tipIPRangeErr),u.validator.addMethod("validStrNoNull",function(e){return Utils.validStrNoNull(e)},u.lang.validate.valRequired),u.validator.addMethod("checkServerID",function(e){return Utils.checkServerID(e)},u.lang.tip.tipCharFmtErr),u.validator.addMethod("validNameContent",function(e){return""==e||Utils.validNameContent(e)},u.lang.tip.tipCharFmtErr),u.validator.addMethod("checkVMPwd",function(e){return!m||Utils.checkServerID(e)},u.lang.tip.tipCharFmtErr),A=u("#frmSetup").validate({focusInvalid:!1,errorElement:"span",errorPlacement:function(e,t){Utils.showJqueryErr(e,t,"div")},success:function(){},rules:{VMPassword:{maxlength:16,validStrNoNull:"",checkVMPwd:""},DeviceID:{maxlength:32,validStrNoNull:"",checkServerID:""},VideoChlID:{maxlength:32,checkServerID:""},AudioChlID:{maxlength:32,checkServerID:""},DeviceName:{maxlength:20,validNameContent:""},ServerID:{maxlength:32,validStrNoNull:"",checkServerID:""},VMIPAddr:{checkIPAddrOrEmpty:"",checkIP1To223OrEmpty:""},VMPort:{integer:!0,required:!0,range:[1025,65535]},BMIPAddr:{checkIPAddrOrEmpty:"",checkIP1To223OrEmpty:""},OnvifStorIpAddr:{checkIPAddrOrEmpty:"",checkIP1To223OrEmpty:""},ExpireTime:{integer:!0,required:!0,range:[3600,36e3]}}})},initPwdChanged:function(){m||(u("#VMPassword").val(""),m=!0)},BMAddressEnable:function(){var e=document.getElementById("BMClose").checked,t=u("#BMIPAddr");(document.getElementById("BMIPAddr").disabled=e)&&(t.val(h.BMIPAddr),A.element(t))},OnvifAddressEnable:function(){var e=u("#OnvifClose").is(":checked"),t=u("#OnvifStorIpAddr");t.prop("disabled",e),e&&(t.val(h.OnvifStorIpAddr),A.element(t))},initVMProtocol:function(){Utils.parseCapOptions("VMProtocol_pub",Capinfo.VMProtocolArr,"mode")},VMprotocol_change:function(){var e=u("#VMProtocol"),t=parseInt(e.val()),a=u("#DeviceNameTR"),r=u("#VideoChlIDTR"),i=u("#AudioChlIDTR"),l=u("#ServerIDTR"),o=u("#vmTbl"),d=u("#VMPasswordTR"),n=u("#regExpireTimeTR"),s=u("#DeviceName"),c=u("#VideoChlID"),v=u("#AudioChlID"),p=u("#ServerID"),P=u("#VMPassword"),I=u("#VMProtocol_private");switch(2<e.val()?I.removeClass("hidden"):(I.addClass("hidden"),I.val("3")),t){case 0:a.addClass("hidden"),r.addClass("hidden"),i.addClass("hidden"),l.addClass("hidden"),o.removeClass("hidden"),d.addClass("hidden"),n.addClass("hidden"),s.val(h.DeviceName),c.val(h.VideoChlID),v.val(h.AudioChlID),p.val(h.ServerID),P.val(C),m=!1;break;case 1:a.removeClass("hidden"),r.removeClass("hidden"),i.removeClass("hidden"),l.removeClass("hidden"),o.removeClass("hidden"),d.removeClass("hidden"),n.removeClass("hidden");break;case 2:o.addClass("hidden"),P.val(C),s.val(h.DeviceName),c.val(h.VideoChlID),v.val(h.AudioChlID),p.val(h.ServerID),u("#VMIPAddr").val(h.VMIPAddr),u("#VMPort").val(h.VMPort),u("input[name='IsUploadEnable'][value='"+h.IsUploadEnable+"']").prop("checked",!0),u("#BMIPAddr").val(h.BMIPAddr),m=!1;break;case 4:case 3:a.removeClass("hidden"),r.removeClass("hidden"),i.removeClass("hidden"),l.removeClass("hidden"),o.removeClass("hidden"),d.removeClass("hidden"),n.addClass("hidden")}A.init()}}))}(jQuery),Frame.currentNameSpace=Config.ManageServer;