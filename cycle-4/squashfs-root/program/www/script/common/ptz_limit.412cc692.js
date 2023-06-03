Config.ptz_limit=function(l){var n={},t={},o=[],s={Latitude:["StatusParam","PTZAbsPostion","Latitude"],Longitude:["StatusParam","PTZAbsPostion","Longitude"],MoveSpeed:["StatusParam","PTZAbsPostion","MoveSpeed"]},i={PtzZoomNum:["StatusParam","PTZAbsZoom","PTZZoomNum"],PtzZoomSpeed:["StatusParam","PTZAbsZoom","PTZZoomSpeed"]};return new(Class.extend({init:function(){Utils.beforeDataLoad(),this.initPage(),Utils.initLang(),this.initEvent(),this.initData(),Utils.afterDataLoad()},initPage:function(){Utils.resetVideoSize(StreamType.LIVE,"recordManager_div_activeX"),Utils.initVideo("recordManager_div_activeX",StreamType.LIVE,RunMode.CONFIG,null,Capinfo.isSupportPTZ)},initData:function(){n={},o=[];for(var e=0;e<Capinfo.MaxVerAngle.length;e++)o[e]=100*Capinfo.MaxVerAngle[e];Utils.LAPI_GetCfgData(LAPI_URL.LAPI_PTZAngleLimitSwitch,n)&&Utils.LAPI_GetCfgData(LAPI_URL.LAPI_PTZAngleLimit,n)?(t=Utils.objectClone(n),0==n.Enable?(document.getElementById("startEA").innerText=l.lang.pub.StartPTZLimit,l("#submit_btn").prop("disabled",!1)):(document.getElementById("startEA").innerText=l.lang.pub.StopPTZLimit,l("#submit_btn").prop("disabled",!0)),this.updateLimitPosBtnStatus()):Utils.disableAll()},initEvent:function(){var e=this;l("#startEA").click(function(){e.enableLimit(this)}),l("div[name='delete']").click(function(){e.clearPtzAbsPosByLimitId(this.id)}),l("div[name='move']").click(function(){e.gotoPtzAbsPosByLimitId(this.id)}),l("img[name='pin']").click(function(){e.getPtzAbsPosByLimitId(this.id)})},submitF:function(){Utils.isObjectEquals(n,t)?Frame.showMsg(!0,l.lang.tip.tipAnyChangeInfo,0):Utils.LAPI_SetCfgData(LAPI_URL.LAPI_PTZAngleLimit,n)&&(t=Utils.objectClone(n))},release:function(){Frame.hiddenVideo(),delete Config.ptz_limit},enableLimit:function(){0==n.Enable?(document.getElementById("startEA").innerText=l.lang.pub.StopPTZLimit,n.Enable=1,l("#submit_btn").prop("disabled",!0)):(document.getElementById("startEA").innerText=l.lang.pub.StartPTZLimit,n.Enable=0,l("#submit_btn").prop("disabled",!1)),Utils.LAPI_SetCfgData(LAPI_URL.LAPI_PTZAngleLimitSwitch,n)},updateLimitPosBtnStatus:function(e){var t=[];void 0===e?t=t.concat("Left","Right","Up","Down"):t.push(e);for(var a=0,s=t.length;a<s;a++){var i=t[a];"Up"==i&&(n[i]!=parseInt(o[0])?(l("#"+i+"Move").removeClass("call-preset-disable").addClass("call-preset-enable"),l("#"+i+"Delete").removeClass("del-disable").addClass("del-enable")):(l("#"+i+"Move").removeClass("call-preset-enable").addClass("call-preset-disable"),l("#"+i+"Delete").removeClass("del-enable").addClass("del-disable"))),"Down"==i&&(n[i]!=parseInt(o[1])?(l("#"+i+"Move").removeClass("call-preset-disable").addClass("call-preset-enable"),l("#"+i+"Delete").removeClass("del-disable").addClass("del-enable")):(l("#"+i+"Move").removeClass("call-preset-enable").addClass("call-preset-disable"),l("#"+i+"Delete").removeClass("del-enable").addClass("del-disable"))),"Left"==i&&(n[i]!=parseInt(o[2])?(l("#"+i+"Move").removeClass("call-preset-disable").addClass("call-preset-enable"),l("#"+i+"Delete").removeClass("del-disable").addClass("del-enable")):(l("#"+i+"Move").removeClass("call-preset-enable").addClass("call-preset-disable"),l("#"+i+"Delete").removeClass("del-enable").addClass("del-disable"))),"Right"==i&&(n[i]!=parseInt(o[3])?(l("#"+i+"Move").removeClass("call-preset-disable").addClass("call-preset-enable"),l("#"+i+"Delete").removeClass("del-disable").addClass("del-enable")):(l("#"+i+"Move").removeClass("call-preset-enable").addClass("call-preset-disable"),l("#"+i+"Delete").removeClass("del-enable").addClass("del-disable")))}},getPtzAbsPos:function(e){var t={},a={},e=Utils.LAPI_GetCfgData(LAPI_URL.PTZAbsPosition,t)&&Utils.LAPI_GetCfgData(LAPI_URL.PTZAbsZoom,a)?(Utils.changeMapToMapByMapping(t,s,e,0),Utils.changeMapToMapByMapping(a,i,e,0),!0):(Frame.showMsg(!1,l.lang.tip.tipGetPtzPosErr),!1);return e},getPtzAbsPosByLimitId:function(e){var t={},e=e.replace("Pin","");this.getPtzAbsPos(t)&&(n[e]="Up"==e||"Down"==e?100*t.Latitude:100*t.Longitude,this.updateLimitPosBtnStatus(e))},gotoPtzAbsPosByLimitId:function(e){var t,a,s=e.replace("Move",""),i={};this.getPtzAbsPos(i)&&(a=n[s],l("#"+e).hasClass("preset_disable")||("Up"==s||"Down"==s?(t=Math.round(100*i.Longitude),Utils.LAPI_SetCfgData(LAPI_URL.PTZAbsoluteMove,{PTZCmd:"32769",Para1:t,Para2:a})):(t=Math.round(100*i.Latitude),Utils.LAPI_SetCfgData(LAPI_URL.PTZAbsoluteMove,{PTZCmd:"32769",Para1:a,Para2:t})),i=Math.round(100*i.PtzZoomNum),Utils.LAPI_SetCfgData(LAPI_URL.PTZAbsoluteMove,{PTZCmd:"32770",Para1:i})))},clearPtzAbsPosByLimitId:function(e){var t=e.replace("Delete","");l("#"+e).hasClass("remove_disable")||("Up"==t&&(n[t]=parseInt(o[0])),"Down"==t&&(n[t]=parseInt(o[1])),"Left"==t&&(n[t]=parseInt(o[2])),"Right"==t&&(n[t]=parseInt(o[3])),this.updateLimitPosBtnStatus(t))}}))}(jQuery),Frame.currentNameSpace=Config.ptz_limit;