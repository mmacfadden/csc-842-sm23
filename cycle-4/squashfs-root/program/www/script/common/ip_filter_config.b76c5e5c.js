Config.ipFilterConfig=function(n){var r={},i={},t=[{fieldId:"rowNum",fieldType:"RowNum"},{fieldId:"IPAddr",fieldType:"text",eventMap:{onchange:function(i){Config.ipFilterConfig.IpAddrese_Change(i)}}},{fieldId:"option",fieldType:"option",option:"<a href='#' class='icon black-del' rowNum=rowNum onclick='Config.ipFilterConfig.delIP($(this).attr(\"rowNum\"));' title='"+n.lang.pub.del+"'></a>"}];return new(Class.extend({init:function(){Utils.beforeDataLoad(),Utils.initLang(),this.initEvent(),this.initData(),Utils.afterDataLoad()},initPage:function(){},initData:function(){r={},Utils.LAPI_GetCfgData(LAPI_URL.IPFilter,r)?(this.initDataView(),Utils.LAPI_CfgToForm("frmSetup",r),i=Utils.objectClone(r)):Utils.disableAll()},initEvent:function(){n("#add").click(function(){Config.ipFilterConfig.addIp(),this.blur()})},submitF:function(){this.checkAllIpAddrValid()&&(Utils.LAPI_FormToCfg("frmSetup",r),!Utils.isObjectEquals(r,i)?Utils.LAPI_SetCfgData(LAPI_URL.IPFilter,r)&&(i=Utils.objectClone(r)):parent.status=n.lang.tip.tipAnyChangeInfo)},release:function(){delete Config.ipFilterConfig},getIPMapList:function(){return r.FilterInfos},isValidIP:function(i){if("0.0.0.0"==i||"255.255.255.255"==i||"127.0.0.1"==i||"224.0.0.1"==i)return!1;if(!Utils.isIPAddress(i))return!1;var t=i.split("."),i=t[0],t=t[3];return!(i<1||223<i)&&0!=t},isIPExist:function(i){for(var t=0;t<r.FilterInfos.length;t++)if(i==r.FilterInfos[t].IPAddr)return!1;return!0},initDataView:function(){IPFilterDataView=new TableView("dataview_tbody",this.getIPMapList,t,5),IPFilterDataView.createDataView(),0<this.getIPMapList().length&&(Utils.checkNavigator("safari")?Utils.safariClick(n("#dataview_tbody").find("tr").get(0)):n("#dataview_tbody").find("tr").get(0).click())},addIp:function(){32==r.FilterInfos.length?alert(n.lang.tip.tipIpAddrMax):this.checkAllIpAddrValid()&&(r.FilterInfos.push({IPAddr:""}),IPFilterDataView.refresh())},checkAllIpAddrValid:function(){for(var i="",t=0;t<r.FilterInfos.length;t++)Config.ipFilterConfig.isValidIP(r.FilterInfos[t].IPAddr)||(i+=t+1+",");return""==i||(i=i.substring(0,i.length-1),alert(n.validator.format(n.lang.tip.tipIpAddrNull,i)),!1)},IpAddrese_Change:function(){var i=Utils.getEvent(),t=(i.srcElement||i.target).id,e=Number(t.replace("IPAddr","")),i=r.FilterInfos[e],e=n("#"+t).val();return Config.ipFilterConfig.isValidIP(e)?this.isIPExist(e)?(""==i.IPAddr&&(r.IPFilterNum=Number(r.IPFilterNum)+1),void(i.IPAddr=e)):(n("#"+t).val(i.IPAddr),void alert(n.lang.tip.tipIpAddrExist)):(n("#"+t).val(i.IPAddr),void alert(n.lang.tip.tipIpAddrErr))},delIP:function(i){""!=r.FilterInfos[i].IPAddr&&(r.IPFilterNum=Number(r.IPFilterNum)-1),r.FilterInfos.splice(i,1),IPFilterDataView.refresh()}}))}(jQuery),Frame.currentNameSpace=Config.ipFilterConfig;