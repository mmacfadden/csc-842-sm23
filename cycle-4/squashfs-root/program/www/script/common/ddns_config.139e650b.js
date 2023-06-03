Config.ddnsConfig=function(n){var s=!1,i=!1,t="@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@",r={},o=null,D={},l={},d={},m={DDNSServerName:["ServerName"],DDNSUserName:["UserName"],DDNSDomainName:["DeviceDomain"]};return new(Class.extend({init:function(){Utils.beforeDataLoad(),this.initPage(),Utils.initLang(),this.initValidator(),this.initData(document.frmSetup),this.initEvent(),Utils.afterDataLoad()},initPage:function(){},initData:function(e){if(e.DDNSPassword.value=t,e.DDNSPasswordConfirm.value=t,l={},Utils.LAPI_GetCfgData(LAPI_URL.DDNS_Cfg,l)){for(var a=0;a<l.Number;a++)D[l.DDNSs[a].Type]=l.DDNSs[a];d=Utils.objectClone(l),this.refreshDDNSTypeOption();e=l.UsedType;Utils.LAPI_CfgToForm("frmSetup",D[e],r,m),Utils.LAPI_CfgToForm("frmSetup",l),this.displayPrivateDDNS(l.UsedType);D[l.UsedType]}else Utils.disableAll()},initEvent:function(){var e=this;n("#UsedType").change(function(){e.changeDDNSType(n("#UsedType").val()),s=!1}),n("#CheckDomain").parent().click(function(){e.checkDomainValid()}),n("#DDNSDomainName").bind("change",function(){e.DDNSDomainName_change()})},submitF:function(){var e;o.form()&&(e=n("#UsedType").val(),Utils.LAPI_FormToCfg("frmSetup",l),Utils.LAPI_FormToCfg("frmSetup",D[e],r,m),s||!Utils.isObjectEquals(l,d)?(s&&(l.RSAPublicKey={},l.RSAPublicKey.RSAPublicKeyE=Frame.RSAPublicKeyE,l.RSAPublicKey.RSAPublicKeyN=Frame.RSAPublicKeyN,D[e].PassWord=Utils.encrypting(n("#DDNSPassword").val(),Frame.RSAKey)),Utils.LAPI_SetCfgData(LAPI_URL.DDNS_Cfg,l,!1,this.callback)):Frame.showMsg(!0,n.lang.tip.tipAnyChangeInfo,0))},callback:function(e){var a=n("#UsedType").val();ResultCode.RESULT_CODE_SUCCEED==e?(s&&(delete l.RSAPublicKey,delete D[a].PassWord),d=Utils.objectClone(l),i=s=!1,n("#DDNSPassword").val(t),n("#DDNSPasswordConfirm").val(t),Frame.showMsg(!0)):ResultCode.RESULT_RASPUBLICKEY_AUTH_ERR==e?(e={},Utils.LAPI_GetCfgData(LAPI_URL.SecurityRSA,e)&&(setMaxDigits(130),Frame.RSAPublicKeyE=e.RSAPublicKeyE,Frame.RSAPublicKeyN=e.RSAPublicKeyN,Frame.RSAKey=new RSAKeyPair(Frame.RSAPublicKeyE,"",Frame.RSAPublicKeyN),l.RSAPublicKey={},l.RSAPublicKey.RSAPublicKeyE=Frame.RSAPublicKeyE,l.RSAPublicKey.RSAPublicKeyN=Frame.RSAPublicKeyN,D[a].PassWord=Utils.encrypting(n("#DDNSPassword").val(),Frame.RSAKey),Utils.LAPI_SetCfgData(LAPI_URL.DDNS_Cfg,l,!1,Config.ddnsConfig.callback))):Frame.showMsg(!1,n.lang.tip.tipSetCfgFail)},release:function(){delete Config.ddnsConfig},displayPrivateDDNS:function(e){var a=this;2==e?(n("#ddnsUserName").parent().addClass("hidden"),n("#ddnsPassword").parent().addClass("hidden"),n("#ddnsPasswordConfirm").parent().addClass("hidden"),n("#CheckDomain").parent().removeClass("hidden"),n("#DDNSDomainName").attr("tip",n.lang.tip.tipDDNSDomainName),n("#deviceAddress").parent().removeClass("hidden"),n.validator.addMethod("checkDDNSDomainName",function(e){return a.checkDDNSDomainName(e)},n.lang.tip.tipDDNSDomainName),this.DDNSDomainName_change()):(n("#ddnsUserName").parent().removeClass("hidden"),n("#ddnsPassword").parent().removeClass("hidden"),n("#ddnsPasswordConfirm").parent().removeClass("hidden"),n("#CheckDomain").parent().addClass("hidden"),n("#DDNSDomainName").attr("tip",n.lang.validate.valUrl),n("#deviceAddress").parent().addClass("hidden"),n.validator.addMethod("checkDDNSDomainName",function(e){return a.checkDDNSDomainName(e)},n.lang.validate.valUrl),n("#testDomainDiv").addClass("hidden"),3==e&&n("#CheckDomain").parent().removeClass("hidden"))},changeDDNSType:function(e){o.resetForm();var a=D[e];Utils.LAPI_CfgToForm("frmSetup",a,r,m),this.displayPrivateDDNS(e)},refreshDDNSTypeOption:function(){for(var e,a="",i={},t=0;t<l.Number;t++)i[l.DDNSs[t].Type]=l.DDNSs[t];for(e in i)a+="<option value='"+e+"'>"+i[e].TypeName+"</option>";n("#UsedType").append(a)},checkDDNSDomainName:function(e){if(2==n("#UsedType").val())return this.checkDDNSDomainNameLength(n("#DDNSDomainName").val());return new RegExp("^((https|http|ftp|rtsp|mms)?://)?(([0-9a-z_!~*'().&=+$%-]+: )?[0-9a-z_!~*'().&=+$%-]+@)?(([0-9]{1,3}.){3}[0-9]{1,3}|([0-9a-z_!~*'()-]+.)*([0-9a-z][0-9a-z-]{0,61})?[0-9a-z].[a-z]{2,6})(:[0-9]{1,4})?((/?)|(/[0-9a-z_!~*'().;?:@&=+$,%#-]+)+/?)$").test(e)},checkDDNSPasswordConfirm:function(e){return n("#DDNSPassword").val()==e},checkUserPwdLength:function(e){return e.replace(/[^\x00-\xff]/g,"xxx").length<=63},DDNSDomainName_change:function(){var e,a;2==n("#UsedType").val()&&(e=n("#DDNSServerName").val(),""!=(a=n("#DDNSDomainName").val())&&(e+="/"+a),n("#deviceAddress").html(e))},checkDDNSDomainNameLength:function(e){return new RegExp(/^[a-zA-Z0-9_-]{4,63}$/).test(e)},checkDomainValid:function(){var e=n("#UsedType").val(),a=n("#DDNSDomainName").val(),i=n("#DDNSUserName").val(),t=s?n("#DDNSPassword").val():"";Utils.LAPI_SetCfgData(LAPI_URL.DDNSDomainCheck,{Type:e,DeviceDomain:a,UserName:i,Password:t},!1)},showResult:function(e,a,i){a?n("#"+e+" a").removeClass("fail").addClass("success"):n("#"+e+" a").removeClass("success").addClass("fail"),n("#"+e+" span").text(i),n("#"+e).removeClass("hidden")},eventDomainCheck:function(e){0==e?this.showResult("testDomainDiv",!0,n.lang.pub.conventionality):1==e?this.showResult("testDomainDiv",!1,n.lang.tip.networkBlock):2==e?this.showResult("testDomainDiv",!1,n.lang.tip.tipOcxInitInvalidUser):3==e?this.showResult("testDomainDiv",!1,n.lang.tip.domainFormatError):4==e?this.showResult("testDomainDiv",!1,n.lang.tip.domainisNotExist):5==e?this.showResult("testDomainDiv",!1,n.lang.tip.serverDefend):6==e&&this.showResult("testDomainDiv",!1,n.lang.tip.tipDomainCheckUnkown)},initValidator:function(){var a=this;n("#DDNSDomainName").attr("tip",n.lang.validate.valUrl),n("#DDNSUserName").attr("tip",n.lang.tip.tipDDNSUserName),n("#DDNSPassword").attr("tip",n.lang.tip.tipDDNSPassword),n("#DDNSPasswordConfirm").attr("tip",n.lang.tip.tipDDNSPasswordConfirm),n.validator.addMethod("checkDDNSDomainName",function(e){return a.checkDDNSDomainName(e)},n.lang.validate.valUrl),n.validator.addMethod("checkDDNSPasswordConfirm",function(e){return a.checkDDNSPasswordConfirm(e)},n.lang.tip.tipDDNSPasswordConfirm),n.validator.addMethod("checkUserPwdLength",function(e){return a.checkUserPwdLength(e)},n.lang.tip.tipDDNSUserName),(o=n("#frmSetup").validate({focusInvalid:!1,errorElement:"span",errorPlacement:function(e,a){Utils.showJqueryErr(e,a,"span")},success:function(e){},rules:{DDNSDomainName:{checkDDNSDomainName:""},DDNSUserName:{checkUserPwdLength:""},DDNSPassword:{checkUserPwdLength:""},DDNSPasswordConfirm:{checkDDNSPasswordConfirm:""}}})).init()},initPwdChanged:function(e){"DDNSPassword"!=e||s?"DDNSPasswordConfirm"!=e||i||(n("#"+e).val(""),i=!0):(n("#"+e).val(""),s=!0)}}))}(jQuery),Frame.currentNameSpace=Config.ddnsConfig;