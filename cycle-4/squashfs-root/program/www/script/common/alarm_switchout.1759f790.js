Config.alarmSwitchout=function(e){var a=null,n=1,r={},l={},u={},o={ChannelId:["ID"],SwitchNameDesc:["Name"],RunMode:["RunMode"],DurationSec:["Duration"]},s=Menu.pageType,c=LAPI_URL.OutputSwitch,d=parseInt(Capinfo.ProductType);return new(Class.extend({init:function(){Utils.beforeDataLoad(),Utils.initLang(),this.initValidator(),this.initPage(),this.initSwitchOut(),this.initData(document.frmSetup),Utils.afterDataLoad()},initPage:function(){(d==DeviceType.DEVICE_IVAGUN?e("#DurationSecms"):e("#DurationSecs")).removeClass("hidden")},initData:function(t){if(r={},n=Number(e("#ChannelId").val()),!Utils.LAPI_GetCfgData(c.replace("id",n),r))return Utils.disableAll(),void Frame.showMsg(!1,e.lang.tip.tipGetCfgFail);l=Utils.objectClone(r),d==DeviceType.DEVICE_IVAGUN?r.Duration:r.Duration=r.Duration/1e3,Utils.LAPI_CfgToForm("frmSetup",r,u,o),0==s&&(e("#planDiv").removeClass("hidden"),Plan.init(LAPI_URL.WeekPlan+"OutputSwitch",e.lang.pub.enbaleOutputPlan))},initEvent:function(){},submitF:function(){var t=Plan.IsChanged();Utils.LAPI_FormToCfg("frmSetup",r,u,o),d==DeviceType.DEVICE_IVAGUN?r.Duration=r.Duration:r.Duration=1e3*r.Duration;var i=!Utils.isObjectEquals(r,l);i||t?a.form()&&(0==s&&t&&Plan.submitF(LAPI_URL.WeekPlan+"OutputSwitch"),i&&(n=Number(e("#ChannelId").val()),Utils.LAPI_SetCfgData(c.replace("id",n),r)&&(l=Utils.objectClone(r)))):Frame.showMsg(!0,e.lang.tip.tipAnyChangeInfo,0)},release:function(){delete Config.alarmSwitchout},initSwitchOut:function(){Utils.parseCapOptionsHidden("ChannelId",Capinfo.switchOutArr,"Channel")},initValidator:function(){var t,i;e("#SwitchNameDesc").attr("tip",e.lang.tip.tipName),i=d==DeviceType.DEVICE_IVAGUN?(e("#DurationSec").attr("tip",e.validator.format(e.lang.tip.tipIntRange,500,5e3)),t=500,5e3):(e("#DurationSec").attr("tip",e.validator.format(e.lang.tip.tipIntRange,1,3600)),t=1,3600),e.validator.addMethod("validStrNoNull",function(t){return Utils.validStrNoNull(t)},e.lang.validate.valRequired),a=e("#frmSetup").validate({debug:!1,focusInvalid:!1,errorElement:"span",errorPlacement:function(t,i){Utils.showJqueryErr(t,i,"span")},success:function(t){},rules:{SwitchNameDesc:{maxlength:20,validStrNoNull:""},DurationSec:{integer:!0,required:!0,range:[t,i]}},submitHandler:this.submitF})}}))}(jQuery),Frame.currentNameSpace=Config.alarmSwitchout;