Config.httpsPage=function(l){var i={},t={},a={},n={EnableHTTPS:["Enable"]};return new(Class.extend({init:function(){Utils.beforeDataLoad(),Utils.initLang(),this.initFile(),this.initEvent(),this.initData(),Utils.afterDataLoad()},initPage:function(){},initData:function(){i={},Utils.LAPI_GetCfgData(LAPI_URL.HTTPS_Cfg,i)?(t=Utils.objectClone(i),Utils.LAPI_CfgToForm("frmSetup",i,a,n)):Utils.disableAll()},initEvent:function(){Video.sdk_viewer&&Video.sdk_viewer.isInstalled&&l("#browse").bind("click",function(){Utils.chooseFileAbsPath("FileNameTxt","*.pem")&&""==l("#FileNameTxt").val()||l("#importBtn").prop("disabled",!1)}),l("#importBtn").bind("click",function(){Config.httpsPage.importCfg()})},submitF:function(){Utils.LAPI_FormToCfg("frmSetup",i,a,n);var e=!Utils.isObjectEquals(i,t);e?e&&Utils.LAPI_SetCfgData(LAPI_URL.HTTPS_Cfg,i)&&(t=Utils.objectClone(i)):parent.status=l.lang.tip.tipAnyChangeInfo},release:function(){delete Config.httpsPage},initFile:function(){l("input#FileName[type='file']").attr("accept",".pem"),Video.sdk_viewer&&Video.sdk_viewer.isInstalled&&l("#FileName").remove()},getFileProcessResult:function(){1==Video.FileProcessResult?this.importCfg_callback(0):2==Video.FileProcessResult?this.importCfg_callback(1):setTimeout(function(){Config.httpsPage.getFileProcessResult()},1e3)},importCfg:function(){if(Video.sdk_viewer&&Video.sdk_viewer.isInstalled)Video.FileProcessResult=0,Video.NetSDKUploadFile(Video,Frame.loginServerIp,Number(Frame.httpPort),Frame.loginUserName,Frame.loginUserPwd,Frame.auzType,LAPI_URL.HTTPS_SSLCERT,l("#FileNameTxt").val(),1),this.getFileProcessResult();else{if(undefined==window.FormData)return alert(l.lang.tip.tipInstallPluginInfo),!1;var e=new FormData;e.append("file",l("#FileName")[0].files[0]),Utils.LAPI_UploadFile(LAPI_URL.HTTPS_SSLCERT,e,this.importCfg_callback)}},importCfg_callback:function(e){e==ResultCode.RESULT_CODE_SUCCEED?Frame.showMsg(!0,l.lang.tip.Uploaded):Frame.showMsg(!1,l.lang.tip.UploadFailed)},chooseFileText:function(e){var i=l("#"+e),t=l("#FileNameTxt"),i=i.val();"FileName"==e&&(t.val(i),l("#importBtn").prop("disabled",!1))}}))}(jQuery),Frame.currentNameSpace=Config.httpsPage;