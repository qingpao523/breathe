import os, sys, subprocess, zipfile, glob
ROOT="/Users/qingpao/.dsh/handoffs/qingpao/breathing-app"
SDK=os.path.expanduser("~/Library/Android/sdk")
BT=os.path.join(SDK,"build-tools","34.0.0")
PLAT=os.path.join(SDK,"platforms","android-34","android.jar")
AND=os.path.join(ROOT,"andapp")
PKG="com/qingpao/app"
OUT=os.path.join(ROOT,"breathe-v1.6.apk")
def sh(n,c):
    p=subprocess.run(c,capture_output=True,text=True)
    o=((p.stdout or "")+(p.stderr or "")).strip()
    if o: print(o[-700:])
    if p.returncode: print("FAIL",n); sys.exit(1)
for d in ["assets","classes","dexout","src/"+PKG]:
    os.makedirs(os.path.join(AND,d),exist_ok=True)
s1="<resources>\n<string name=\"app_name\">\u547c\u5438</string>\n"
s2="<string name=\"app_name2\">\u547c\u5438\u6d4b\u8bd5</string>\n</resources>\n"
open(os.path.join(ROOT,"android","res","values","strings.xml"),"w",encoding="utf-8").write(s1+s2)
open(os.path.join(AND,"assets","index.html"),"w",encoding="utf-8").write(open(os.path.join(ROOT,"android","assets","index.html"),encoding="utf-8").read())
m1="<?xml version=\"1.0\" encoding=\"utf-8\"?>\n<manifest xmlns:android=\"http://schemas.android.com/apk/res/android\" package=\"com.qingpao.app\" android:versionCode=\"16\" android:versionName=\"1.6\">\n"
m2="<uses-sdk android:minSdkVersion=\"26\" android:targetSdkVersion=\"34\"/>\n<uses-permission android:name=\"android.permission.VIBRATE\"/>\n<application android:label=\"@string/app_name\" android:icon=\"@mipmap/ic_launcher\" android:roundIcon=\"@mipmap/ic_launcher_round\">\n"
m3="<activity android:name=\".MainActivity\" android:exported=\"true\"><intent-filter><action android:name=\"android.intent.action.MAIN\"/><category android:name=\"android.intent.category.LAUNCHER\"/></intent-filter></activity></application></manifest>\n"
m2=m2.replace('VIBRATE"/>','VIBRATE"/><uses-permission android:name="android.permission.POST_NOTIFICATIONS"/>')
m3=m3.replace('</activity>','</activity><receiver android:name=".AlarmReceiver" android:exported="false"/>')
open(os.path.join(AND,"AndroidManifest.xml"),"w",encoding="utf-8").write(m1+m2+m3)
j1="package com.qingpao.app;\nimport android.app.Activity; import android.os.Bundle; import android.widget.TextView;\nimport android.webkit.WebView; import android.webkit.WebSettings; import android.webkit.WebViewClient;\nimport android.webkit.JavascriptInterface; import android.os.Vibrator; import android.os.VibrationEffect; import android.widget.Toast; import android.view.WindowManager;\n"
j2="public class MainActivity extends Activity {\npublic class Bridge {\n @JavascriptInterface public void vibrate(int ms){ try{ Vibrator v=(Vibrator)getSystemService(VIBRATOR_SERVICE); if(v!=null) v.vibrate(VibrationEffect.createOneShot(ms, VibrationEffect.DEFAULT_AMPLITUDE)); }catch(Throwable e){} }\n @JavascriptInterface public void keepScreenOn(final boolean on){ runOnUiThread(new Runnable(){ public void run(){ try{ if(on) getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON); else getWindow().clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON); }catch(Throwable e){} } }); }\n @JavascriptInterface public void toast(final String msg){ runOnUiThread(new Runnable(){ public void run(){ try{ Toast.makeText(MainActivity.this, msg, Toast.LENGTH_SHORT).show(); }catch(Throwable e){} } }); }\n}\n@Override protected void onCreate(Bundle b){ super.onCreate(b);\n try {\n  WebView w=new WebView(this); WebSettings s=w.getSettings();\n  s.setJavaScriptEnabled(true); s.setDomStorageEnabled(true); s.setAllowFileAccess(true); s.setMediaPlaybackRequiresUserGesture(false);\n  w.setWebViewClient(new WebViewClient());\n  w.addJavascriptInterface(new Bridge(),\"AndroidBridge\");\n  w.loadUrl(\"file:///android_asset/index.html\");\n  setContentView(w);\n } catch (Throwable e) {\n  TextView t=new TextView(this);\n  t.setText(\"WEBVIEW FAILED\\n\"+e.getClass().getName()+\"\\n\"+e.getMessage());\n  setContentView(t);\n }\n}\n}\n"
J_BRIDGE=r''' @JavascriptInterface public boolean hasNotifPermission(){ try{ if(Build.VERSION.SDK_INT < 33) return true; return checkSelfPermission("android.permission.POST_NOTIFICATIONS")==PackageManager.PERMISSION_GRANTED; }catch(Throwable e){ return false; } }
 @JavascriptInterface public void setReminder(final String kind,final int hour,final int minute,final boolean on){ try{ if(kind==null) return; final String k=("sleep".equals(kind))?"sleep":"ride"; runOnUiThread(new Runnable(){ public void run(){ try{ if(on){ boolean ok=(Build.VERSION.SDK_INT < 33) || (checkSelfPermission("android.permission.POST_NOTIFICATIONS")==PackageManager.PERMISSION_GRANTED); if(ok){ AlarmReceiver.schedule(MainActivity.this,k,hour,minute); } else { pendingKind=k; pendingHour=hour; pendingMinute=minute; requestPermissions(new String[]{"android.permission.POST_NOTIFICATIONS"},REQ_NOTIF); } } else { pendingKind=null; pendingHour=0; pendingMinute=0; AlarmReceiver.cancel(MainActivity.this,k); } }catch(Throwable e){} } }); }catch(Throwable e){} }
 @JavascriptInterface public void cancelReminder(String kind){ try{ if(kind==null) return; final String k=("sleep".equals(kind))?"sleep":"ride"; runOnUiThread(new Runnable(){ public void run(){ try{ pendingKind=null; pendingHour=0; pendingMinute=0; AlarmReceiver.cancel(MainActivity.this,k); }catch(Throwable e){} } }); }catch(Throwable e){} }
'''
J_PERM=r''' @Override public void onRequestPermissionsResult(int requestCode,String[] permissions,int[] grantResults){
  super.onRequestPermissionsResult(requestCode,permissions,grantResults);
  try{
    if(requestCode==REQ_NOTIF){
      boolean ok=grantResults.length>0 && grantResults[0]==PackageManager.PERMISSION_GRANTED;
      if(ok){
        if(pendingKind==null){ } else { AlarmReceiver.schedule(this,pendingKind,pendingHour,pendingMinute); }
      } else {
        if(pendingKind==null){ } else {
          Toast.makeText(MainActivity.this,"\u9700\u8981\u901a\u77e5\u6743\u9650\uff0c\u63d0\u9192\u5df2\u5173\u95ed",Toast.LENGTH_SHORT).show();
          final String k=pendingKind;
          if(web==null){ } else {
            web.post(new Runnable(){ public void run(){ try{ web.evaluateJavascript("window.onReminderPermissionResult&&window.onReminderPermissionResult('"+k+"',false)",null); }catch(Throwable e){} } });
          }
        }
      }
      pendingKind=null;
    }
  }catch(Throwable e){}
 }
'''
J_RECV=r'''package com.qingpao.app;
import android.app.AlarmManager;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import java.util.Calendar;
public class AlarmReceiver extends BroadcastReceiver {
  static final String CH_ID = "breathe_reminders";
  static int req(String kind){ return "sleep".equals(kind) ? 2002 : 2001; }
  static PendingIntent pi(Context c, String kind, int hour, int minute){
    Intent i = new Intent(c, AlarmReceiver.class);
    i.setAction("breathe.reminder." + kind);
    i.putExtra("kind", kind);
    i.putExtra("hour", hour);
    i.putExtra("minute", minute);
    return PendingIntent.getBroadcast(c, req(kind), i, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
  }
  static long nextAt(int hour, int minute){
    Calendar c = Calendar.getInstance();
    c.set(Calendar.HOUR_OF_DAY, hour);
    c.set(Calendar.MINUTE, minute);
    c.set(Calendar.SECOND, 0);
    c.set(Calendar.MILLISECOND, 0);
    if(c.getTimeInMillis() <= System.currentTimeMillis()) c.add(Calendar.DAY_OF_YEAR, 1);
    return c.getTimeInMillis();
  }
  static void schedule(Context ctx, String kind, int hour, int minute){
    try{
      AlarmManager am = (AlarmManager) ctx.getSystemService(Context.ALARM_SERVICE);
      if(am == null) return;
      am.setAndAllowWhileIdle(AlarmManager.RTC_WAKEUP, nextAt(hour, minute), pi(ctx, kind, hour, minute));
    }catch(Throwable e){}
  }
  static void cancel(Context ctx, String kind){
    try{
      AlarmManager am = (AlarmManager) ctx.getSystemService(Context.ALARM_SERVICE);
      if(am == null){} else { am.cancel(pi(ctx, kind, 0, 0)); }
      NotificationManager nm = (NotificationManager) ctx.getSystemService(Context.NOTIFICATION_SERVICE);
      if(nm == null){} else { nm.cancel(req(kind)); }
    }catch(Throwable e){}
  }
  static void notifyNow(Context ctx, String kind){
    try{
      NotificationManager nm = (NotificationManager) ctx.getSystemService(Context.NOTIFICATION_SERVICE);
      if(nm == null) return;
      NotificationChannel ch = new NotificationChannel(CH_ID, "\u547c\u5438\u63d0\u9192", NotificationManager.IMPORTANCE_DEFAULT);
      ch.setDescription("\u9a91\u884c\u65e5\u4e0e\u7761\u524d\u63d0\u9192");
      nm.createNotificationChannel(ch);
      Intent open = new Intent(ctx, MainActivity.class);
      open.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);
      PendingIntent content = PendingIntent.getActivity(ctx, req(kind), open, PendingIntent.FLAG_UPDATE_CURRENT | PendingIntent.FLAG_IMMUTABLE);
      String title = "sleep".equals(kind) ? "\u7761\u524d\u63d0\u9192" : "\u9a91\u884c\u65e5\u63d0\u9192";
      String text = "sleep".equals(kind) ? "\u8be5\u505a 4-7-8 \u52a9\u7720\u4e86" : "\u51fa\u53d1\u524d 30 \u5206\u949f\uff0c\u5148\u505a\u4e00\u8f6e\u547c\u5438";
      Notification.Builder b = new Notification.Builder(ctx, CH_ID);
      b.setSmallIcon(android.R.drawable.ic_lock_idle_alarm).setContentTitle(title).setContentText(text).setContentIntent(content).setAutoCancel(true);
      nm.notify(req(kind), b.build());
    }catch(Throwable e){}
  }
  @Override public void onReceive(Context context, Intent intent){
    try{
      String kind = (intent == null) ? null : intent.getStringExtra("kind");
      if(kind == null) kind = "ride";
      notifyNow(context, kind);
      int h = (intent == null) ? 7 : intent.getIntExtra("hour", 7);
      int m = (intent == null) ? 0 : intent.getIntExtra("minute", 0);
      schedule(context, kind, h, m);
    }catch(Throwable e){}
  }
}
'''
j1=j1.replace('import android.view.WindowManager;','import android.view.WindowManager; import android.os.Build; import android.content.pm.PackageManager;')
j2=j2.replace('public class MainActivity extends Activity {','public class MainActivity extends Activity { private WebView web; private String pendingKind=null; private int pendingHour=7; private int pendingMinute=0; static final int REQ_NOTIF=9911;')
j2=j2.replace('WebView w=new WebView(this);','web=new WebView(this);')
j2=j2.replace('setContentView(w);','setContentView(web);')
j2=j2.replace('WebSettings s=w.getSettings();','WebSettings s=web.getSettings();')
j2=j2.replace('w.setWebViewClient','web.setWebViewClient')
j2=j2.replace('w.addJavascriptInterface','web.addJavascriptInterface')
j2=j2.replace('w.loadUrl','web.loadUrl')
j2=j2.replace('public class Bridge {','public class Bridge {'+J_BRIDGE)
j2=j2.replace('@Override protected void onCreate(Bundle b){',J_PERM+'@Override protected void onCreate(Bundle b){',1)
open(os.path.join(AND,"src",PKG,"AlarmReceiver.java"),"w",encoding="utf-8").write(J_RECV)
open(os.path.join(AND,"src",PKG,"MainActivity.java"),"w",encoding="utf-8").write(j1+j2)
sh("res",[os.path.join(BT,"aapt2"),"compile","--dir",os.path.join(ROOT,"android","res"),"-o",os.path.join(AND,"res.zip")])
sh("link",[os.path.join(BT,"aapt2"),"link","-o",os.path.join(AND,"base.apk"),"-I",PLAT,"--manifest",os.path.join(AND,"AndroidManifest.xml"),"-A",os.path.join(AND,"assets"),os.path.join(AND,"res.zip"),"--min-sdk-version","26","--target-sdk-version","34"])
sh("javac",["javac","-source","8","-target","8","-nowarn","-cp",PLAT,"-d",os.path.join(AND,"classes")]+glob.glob(os.path.join(AND,"src",PKG,"*.java")))
sh("d8",[os.path.join(BT,"d8"),"--release","--min-api","26","--lib",PLAT,"--output",os.path.join(AND,"dexout"),]+glob.glob(os.path.join(AND,"classes","**","*.class"),recursive=True))
z=zipfile.ZipFile(os.path.join(AND,"base.apk"),"a",zipfile.ZIP_STORED); z.write(os.path.join(AND,"dexout","classes.dex"),"classes.dex"); z.close()
sh("align",[os.path.join(BT,"zipalign"),"-f","4",os.path.join(AND,"base.apk"),os.path.join(AND,"aligned.apk")])
sh("sign",[os.path.join(BT,"apksigner"),"sign","--ks",os.path.expanduser("~/.android/debug.keystore"),"--ks-pass","pass:android","--key-pass","pass:android","--ks-key-alias","androiddebugkey","--out",OUT,os.path.join(AND,"aligned.apk")])
print("APP OK",OUT,os.path.getsize(OUT))
