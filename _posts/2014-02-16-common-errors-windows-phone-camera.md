---
title: Common errors in Windows Phone camera apps
disqus: y
---
<p><br/><br />
Recently, while working on my smart resize apps, I ran into a bug of crashes and freezes related to using the camera API. I think I managed to fix them, so I'd like to share some techniques I used.</p>
<p>If you are making a Windows Phone app using the camera, you probably copied the <a href="http://msdn.microsoft.com/en-us/library/windowsphone/develop/hh202956(v=vs.105).aspx">basic code from the MSDN documentation</a>, and have something along the lines of :</p>

```csharp
cam = new Microsoft.Devices.PhotoCamera(CameraType.Primary);
// Setup camera events...
cam.Initialized += ...;
cam.CaptureCompleted += ...;
cam.CaptureImageAvailable += ...;
cam.CaptureThumbnailAvailable += ...;
// Setup shutter key events...
...;
// Display camera live feed
viewfinderBrush.SetSource(cam);
```

<p>This works fine, but the asynchronous nature of the camera (which takes some time to load, especially with larger lenses like on the Lumia 1020) means that if you aren't careful, you can get the app to crash or the camera to freeze.<br />
<br/><br />
<b>1. The app crashes when navigating back and forth between pages.</b></p>
<p>If you navigate out of a page which uses the camera before it's loaded and back in, under certain random condition the app will terminate in an UnhandledException. The stacktrace may be something unhelpful like :</p>

```
at System.Threading.Tasks.Task.ThrowIfExceptional(Boolean includeTaskCanceledExceptions)
at System.Threading.Tasks.Task.Wait(Int32 millisecondsTimeout, CancellationToken cancellationToken)
at Microsoft.Devices.Camera.SetAppropriatePreviewResolution(Size captureResolution)
at Microsoft.Devices.Camera.<>c__DisplayClass2.<InitializeVideoSession>b__0()
```

<p>or possibly</p>

```
at Windows.Phone.Media.Capture.PhotoCaptureDevice.GetProperty(Guid propertyId)
at Microsoft.Devices.Camera.GetVideoPortName()
at Microsoft.Devices.Camera.<>c__DisplayClass2.<InitializeVideoSession>b__1()
```

<p>This is quite difficult to fix. It's useful to remove event handlers when the camera is disposed and check for the status of the camera (if it's been disposed) when the event handlers are called, but that might not quite fix it. My solution is to <b>hide navigation controls while the camera is loading</b>. i.e., if there are buttons on your page, or if you use the ApplicationBar, set the visibility to false until Camera.Initialized is called.</p>
<p>Note : You must hide the ApplicationBar and any other button whenever the page is navigated to (OnNavigatedTo), not just in the constructor! The constructor won't get called if you go back to a page using the back button.<br />
<br/><br />
<b>2. The camera feed freezes when switching between the front and back camera.</b></p>
<p>In fact, the whole app might be freezing. Again, this is due to the user interacting with the app too quickly, before either camera has been properly loaded.</p>
<p>If you have a button to toggle between the primary (back) and front-facing cameras, you must make sure to test what happens if you double tap on that button. If it creates a camera (as in the code shown above) more than once, freezes and crashes could occur.</p>
<p>For simple on-screen button, you can just hide or disable the button. Alternatively, you can set a boolean flag to indicate whether the camera has been initialized and do nothing on button process if the flag is false.</p>
<p>If you have the button in the ApplicationBar, note that setting ApplicationBar.IsVisible to false is <b>not sufficient</b>. The ApplicationBar takes half a second to disappear since it is animated, and taps on the button can still occur during the animation. You cannot assume that the event handler for buttons in the ApplicationBar will not be triggered the moment ApplicationBar.IsVisible is set to false.</p>

```csharp
private void ToggleCamera(object sender, EventArgs e)
{
    // The user might double tap on the buttom, which can freeze the
    // camera. So this condition is here to prevent double taps.
    if (!ApplicationBar.IsVisible)
        return;
    ApplicationBar.IsVisible = false;
    switch (prevCameraType)
    {
        case CameraType.Primary:
    ...
```

<p><br/><br />
<b>3. The app doesn't freeze or crash, but nothing shows up on the viewfinder.</b></p>
<p>There are a lot of possible causes as to why nothing would be displayed in the camera's viewfinder. I focus on the case where it happens randomly, usually following user interaction.</p>
<p>You probably have events that get triggered when tapping on the viewfinder and/or pressing the shutter keys (and you should!). When those events are triggered while the camera isn't loaded can cause crash (UnhandledException), freezes, or simply a blank viewfinder. So you must make sure to remove those events OnNavigatedFrom (leaving the app) <b>and</b> when you toggle between camera types, and only set the events when the camera is initialized.</p>
<p>It is especially easy for the user to accidentally tap on the viewfinder when tapping the toggle camera button.</p>

```csharp
private void Camera_Initialized(object sender, CameraOperationCompletedEventArgs e)
{
    // Show error when this happens.
    if (!e.Succeeded)
        return;

    this.Dispatcher.BeginInvoke(delegate()
    {
        // We are ready to let the user use the camera.
        ApplicationBar.IsVisible = true;

        // The camera is ready to take events.
        ViewfinderCanvas.Tap += ViewfinderCanvas_Tapped;
        CameraButtons.ShutterKeyPressed += OnShutterKeyPressed;
        CameraButtons.ShutterKeyHalfPressed += OnShutterKeyHalfPressed;
        CameraButtons.ShutterKeyReleased += OnShutterKeyReleased;
    });
}

// This should get called when leaving the page or switching
// between front/back camera.
private void DisposeCamera()
{
    if (camera != null)
    {
        camera.CaptureImageAvailable -= Camera_CaptureImageAvailable;
        camera.Initialized -= Camera_Initialized;
        camera.AutoFocusCompleted -= Camera_AutoFocusCompleted;
        camera.Dispose();
    }

    ViewfinderCanvas.Tap -= ViewfinderCanvas_Tapped;

    CameraButtons.ShutterKeyPressed -= OnShutterKeyPressed;
    CameraButtons.ShutterKeyHalfPressed -= OnShutterKeyHalfPressed;
    CameraButtons.ShutterKeyReleased -= OnShutterKeyReleased;
}
```

<p>I hope you found something helpful for your app! Best of luck in your debugging!</p>
