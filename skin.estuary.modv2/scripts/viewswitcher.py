import time
import xbmc
import xbmcgui
import xbmcaddon

if __name__ == '__main__':
    # init props
    xbmcgui.Window(10000).setProperty("ServiceSkinViewswitcherDone","0")
    xbmcgui.Window(10000).setProperty("ServiceSkinViewswitcherLastContent",xbmc.getInfoLabel("Container.Content"))
    
    trans_title = xbmc.getLocalizedString(369)
    #dlg = xbmcgui.Dialog()
    #dlg.ok("Title",trans_title)
    
    monitor = xbmc.Monitor()
    xbmc.log("service.skin.viewswitcher - Start service", level=xbmc.LOGNOTICE)
    while not monitor.abortRequested():
        # Sleep/wait for abort for 10 seconds
        if monitor.waitForAbort(0.5):
            # Abort was requested while waiting. We should exit
            break
        if not xbmc.getCondVisibility("!Skin.HasSetting(ForcedViews.Enabled)") == 1:
            current_content = xbmc.getInfoLabel("Container.Content")
            path = ""
            if current_content == "movies":
                path = xbmc.getInfoLabel("Container.FolderName")
                setname = xbmc.getInfoLabel("ListItem.Set")
                if (str(trans_title) != str(path)):
                    current_content = "setmovies"
                    #dlg = xbmcgui.Dialog()
                    #dlg.ok("Set",str(path) + " - " + trans_title)

            if current_content in "movies|sets|setmovies|tvshows|seasons|episodes|albums|artists|songs|musicvideos|pictures|videos|files":
                if (current_content != xbmcgui.Window(10000).getProperty("ServiceSkinViewswitcherLastContent")):
                    # content type has changed - reset "done"
                    xbmcgui.Window(10000).setProperty("ServiceSkinViewswitcherDone","0")
                current_view_label = xbmc.getInfoLabel("Container.Viewmode").decode("utf-8")
                dest_view_id = xbmc.getInfoLabel("Skin.String(SkinHelper.ForcedViews.%s)" % current_content).decode("utf-8")
                dest_view_label = xbmc.getInfoLabel("Skin.String(SkinHelper.ForcedViews.%s.label)" % current_content).decode("utf-8")
                if current_view_label == dest_view_label:
                    xbmcgui.Window(10000).setProperty("ServiceSkinViewswitcherDone","1")
                    xbmcgui.Window(10000).setProperty("ServiceSkinViewswitcherLastContent",current_content)
                if dest_view_id != "" and xbmcgui.Window(10000).getProperty("ServiceSkinViewswitcherDone") != "1":
                    if current_view_label != dest_view_label:
                        #dlg = xbmcgui.Dialog()
                        #dlg.ok("Path:","current: " + current_content + " old: " + xbmcgui.Window(10000).getProperty("ServiceSkinViewswitcherLastContent"))
                        xbmc.executebuiltin("Container.SetViewMode(%s)" % dest_view_id)
                        xbmc.log("service.skin.viewswitcher - Cur label: " + current_view_label, level=xbmc.LOGNOTICE)
                        xbmc.log("service.skin.viewswitcher - Cur id: " + str(current_content), level=xbmc.LOGNOTICE)
                        xbmc.log("service.skin.viewswitcher - Switching to:", level=xbmc.LOGNOTICE)
                        xbmc.log("service.skin.viewswitcher - Dest label: " + str(dest_view_label), level=xbmc.LOGNOTICE)
                        xbmc.log("service.skin.viewswitcher - Dest id: " + str(dest_view_id), level=xbmc.LOGNOTICE)
                        xbmcgui.Window(10000).setProperty("ServiceSkinViewswitcherDone","1")
                        xbmcgui.Window(10000).setProperty("ServiceSkinViewswitcherLastContent",current_content)
                        # give kodi time to relax :-)
                        time.sleep(1)
