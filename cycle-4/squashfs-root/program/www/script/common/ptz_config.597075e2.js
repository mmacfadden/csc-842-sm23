Config.ptz_config=function(r){var t={},a={},l=[],f=[],n={},i={Enable:["Enabled"],Action:["Mode"],ID:["Param"],Time:["Time"]};return new(Class.extend({init:function(){Utils.beforeDataLoad(),this.initPage(),Utils.initLang(),this.initValidator(),this.initEvent(),this.initData(),Utils.afterDataLoad()},initPage:function(){Capinfo.isSupportTrackRecord&&r("#Action").append('<option value="2" lang="watchToPrePositionCruise"></option>')},initData:function(){t={},n={},Utils.LAPI_GetCfgData(LAPI_URL.PtzGuardCfg,t)?(Number(t.Time)<1&&(t.Time=60),a=Utils.objectClone(t),r("#Action").val(t.Mode),this.getTrackInfo(),this.action_change(),Utils.LAPI_CfgToForm("frmSetup",t,n,i)):Utils.disableAll()},initEvent:function(){var t=this;r("#Action").change(function(){t.action_change()})},submitF:function(){validator.form()&&(Utils.LAPI_FormToCfg("frmSetup",t,n,i),!Utils.isObjectEquals(t,a)?Utils.LAPI_SetCfgData(LAPI_URL.PtzGuardCfg,t)&&(a=Utils.objectClone(t)):Frame.showMsg(!0,r.lang.tip.tipAnyChangeInfo,0))},release:function(){delete Config.ptz_config},initValidator:function(){r("#Time").attr("tip",r.validator.format(r.lang.tip.tipIntRange,1,3600)),validator=r("#frmSetup").validate({focusInvalid:!1,errorElement:"span",errorPlacement:function(t,a){Utils.showJqueryErr(t,a,"div")},success:function(t){},rules:{Time:{integer:!0,required:!0,range:[1,3600]}}}),validator.init()},getTrackInfo:function(){var t={},a={},n={};if(Utils.LAPI_GetCfgData(LAPI_URL.PTZPatrol,a)&&Utils.LAPI_GetCfgData(LAPI_URL.PTZRoutePatrol,n)){for(var i=0;i<a.Num;i++){t["Track"+(i+1)+"CruiseNum"]=a.PatrolInfos[i].Num,t["Track"+(i+1)+"TrackId"]=a.PatrolInfos[i].ID+1,t["Track"+(i+1)+"TrackName"]=a.PatrolInfos[i].Name;for(var o=0;o<a.PatrolInfos[i].Num;o++)t["Track"+(i+1)+"Action"+(o+1)]=a.PatrolInfos[i].Actions[o].Type,t["Track"+(i+1)+"Duration"+(o+1)]=0==a.PatrolInfos[i].Actions[o].Duration?a.PatrolInfos[i].Actions[o].Para3:a.PatrolInfos[i].Actions[o].Duration,t["Track"+(i+1)+"Speed"+(o+1)]=0==a.PatrolInfos[i].Actions[o].Para1?a.PatrolInfos[i].Actions[o].Para2:a.PatrolInfos[i].Actions[o].Para1,t["Track"+(i+1)+"PresetId"+(o+1)]=a.PatrolInfos[i].Actions[o].PresetID}l=[];for(var e=1;"undefined"!=typeof t["Track"+e+"TrackId"];e++){var r="Track"+e,s=t[r+"TrackId"],c={};c.id=s,c.name=t[r+"TrackName"],l.push(c)}for(e=0;e<n.Num;e++)(c={}).id=n.RecordedPatrolInfos[e].ID+1,f.push(c)}},makeSelectList:function(t){var a=r("#ID");a.empty(),a.append("<option value='0xFFFFFFFF' title='"+r.lang.pub.none+"'>["+r.lang.pub.none+"]</option>");for(var n=0,i=t.length;n<i;n++){var o,e=t[n];e&&(e=(o=e.id)+"["+("undefined"==typeof e.name?r.lang.pub.modeRoute:e.name)+"]",a.append("<option value='"+o+"' title='"+e+"'>"+e+"</option>"))}},action_change:function(){var t=r("#Action").val(),a=r("#position").html();0==t?(a=a.replace("-1","0xFFFFFFFF"),r("#ID").html(a)):1==t?this.makeSelectList(l):2==t&&this.makeSelectList(f)}}))}(jQuery),Frame.currentNameSpace=Config.ptz_config;