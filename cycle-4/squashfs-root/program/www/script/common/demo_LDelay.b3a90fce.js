Utils.$package("demoLDelay"),demoLDelay=function(u){return new(Class.extend({LAPI_SetCfgNoTip:function(n,s){var e=(new Date).getTime();""==Utils.getCookie("WebLoginHandle")&&Utils.setCookie("WebLoginHandle",e);var a=s.authorization;void 0!==a&&delete s.authorization,null!=top.responseAuthInfo&&(a=Utils.web_Digest(top.responseAuthInfo,n,"PUT"));var e=u.toJSON(s)+"\r\n",i=!0,r=this;return u.ajax({type:"PUT","async":!1,url:n,data:e,dataType:"json",beforeSend:function(e){void 0!==a&&e.setRequestHeader("Authorization",a)},success:function(e,t,o){i=e.Response.StatusCode==ResultCode.RESULT_CODE_SUCCEED,3==e.Response.ResponseCode&&(e.Response.SubResponseCode,"200"==o.status&&(top.responseAuthInfo=o.getResponseHeader("WWW-Authenticate")),a=Utils.web_Digest(top.responseAuthInfo,n,"PUT"),"false"!=top.stale||n==LAPI_URL.webLoginCfg?(s.authorization=a,i=r.LAPI_SetCfgNoTip(n,s)):(o=u.lang.tip.tipUserInfoChanged,top.isAlertPwdChanged||(Frame.pageLogout(o),top.isAlertPwdChanged=!0)))},error:function(){i=!1}}),i},LAPI_GetCfgNoTip:function(n,s){var e=(new Date).getTime();""==Utils.getCookie("WebLoginHandle")&&Utils.setCookie("WebLoginHandle",e);var a=s.authorization;void 0!==a&&delete s.authorization,null!=top.responseAuthInfo&&(a=Utils.web_Digest(top.responseAuthInfo,n,"GET"));var i=!0,r=this;return n=0<=n.indexOf("?")?n+"&randomKey="+(new Date).getTime():n+"?randomKey="+(new Date).getTime(),u.ajax({type:"GET","async":!1,url:n,data:"",dataType:"json",beforeSend:function(e){void 0!==a&&e.setRequestHeader("Authorization",a)},success:function(e,t,o){i=e.Response.StatusCode==ResultCode.RESULT_CODE_SUCCEED,3==e.Response.ResponseCode?(e.Response.SubResponseCode,"200"==o.status&&(top.responseAuthInfo=o.getResponseHeader("WWW-Authenticate")),a=Utils.web_Digest(top.responseAuthInfo,n,"GET"),"false"!=top.stale?(s.authorization=a,i=r.LAPI_GetCfgNoTip(n,s)):(o=u.lang.tip.tipUserInfoChanged,top.isAlertPwdChanged||(Frame.pageLogout(o),top.isAlertPwdChanged=!0))):i&&u.extend(!0,s,e.Response.Data)},error:function(){i=!1}}),i},getCfgDataNoTip:function(e,t,o){var n=!1,t=Video.sdk_viewer.ViewerAxGetConfig20(e,t,""),t=Utils.getSDKParam(t);return ResultCode.RESULT_CODE_SUCCEED==t[0]&&(Utils.sdkAddCfg(o,t[1]),n=!0),n}}))}(jQuery);