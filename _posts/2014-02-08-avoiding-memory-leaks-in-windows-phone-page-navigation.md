---
title: Avoiding memory "leaks" in Windows Phone page navigation
disqus: y
---
<p>The nice thing about programming with managed languages such as C# or Java is that we don't need to worry about memory leaks. After all, we have a nice butler called the garbage collector to take care of things for us. Or at least, we <em>usually</em> don't. It's still possible to get memory "leaks".</p>
<p>I'm writing "leak" in quotation marks as they are not exactly the same as your classical C-style leaks, where a block of memory has been allocated but there is no pointer pointing to that address anymore. Rather, unless your code is calling a native component (this might happen if you're using a 3rd party-library which uses native code for speed, such as <a href="http://developer.nokia.com/lumia/nokia-apis/imaging">Nokia's Imaging SDK</a>) the opposite is often quite true : you <em>have</em> a pointer to a block of memory that you don't actually needed and because this pointer exists, the garbage collector can't get rid of it.</p>
<p>Here's an example of something that happened in my recent developer ventures. Navigating back and forth between two pages would give me an OutOfMemoryException. What would be the cause?</p>
<p>The first step is to measure memory usage. This page describes <a href="http://developer.nokia.com/community/wiki/Techniques_for_memory_analysis_of_Windows_Phone_apps">techniques to do so</a> better than I could in a blog post, but the jist of it is that you either use Visual Studio's memory profiler or the static variables</p>

```csharp
DeviceStatus.ApplicationCurrentMemoryUsage
DeviceStatus.ApplicationPeakMemoryUsage
DeviceStatus.ApplicationMemoryUsageLimit
```

<p>Finding the exact place where the memory leak occurs can be tricky, especially if the memory being leaked occurs in small pieces throughout the code. In that case, finding one place where the memory leaks is still good enough of a starting point. A way to do this is to add a watch in the visual studio debugger for <code>DeviceStatus.ApplicationCurrentMemoryUsage</code> that you can monitor as you step through your code.</p>
<p>In my case, the memory usage increased significantly after the following lines :</p>

```csharp
protected override void OnNavigatedTo(NavigationEventArgs e)
{
    // ...

    NavigationData.OriginalImage = NavigationData.OriginalImage.Rotate(
        360 - NavigationData.RotationAngle);
    ImageVertical.Source = NavigationData.OriginalImage;

    // ...
}
```

<p>It's kind of obvious that creating a new image would involve a few megabytes - that doesn't indicate that it involves a memory leak. However, since I am replacing the original image with the rotating image, I would expect the original image to be freed. However, in managed languages, memory does not get freed the moment it is no longer used, so we need to force a call to the garbage collector.</p>

```csharp
NavigationData.OriginalImage = NavigationData.OriginalImage.Rotate(
    360 - NavigationData.RotationAngle);
ImageVertical.Source = NavigationData.OriginalImage;
GC.Collect();
```

<p>Calling the garbage collector does not free memory - then it means that we still have a pointer to the original image somewhere. Where? Just to confirm that the leak isn't due to a faulty implementation of WriteableBitmap.Rotate, which comes from the third-party extension WriteableBitmapEx, or Image.Source, I run that code inside a loop.</p>

```csharp
for (int i = 0; i < 100; i++)
{
    NavigationData.OriginalImage = NavigationData.OriginalImage.Rotate(
        360 - NavigationData.RotationAngle);
    ImageVertical.Source = NavigationData.OriginalImage;
    GC.Collect();
}
```

<p>Peak memory increases, but no leak.</p>
<p>Since I don't use <code>NavigationData.OriginalImage</code> anywhere else in code that gets reached at this point, then it must have something to do with page navigation.</p>
<p>Placing a breakpoint in the constructor of the page, I notice the constructor gets called every time the page is navigated to. If the old page were to remain alive, then <code>ImageVertical.Source</code> would still hold a pointer to the original images.</p>
<p>And that's indeed where the problem lies. Using :</p>

```csharp
NavigationService.Navigate(new Uri(page, UriKind.Relative));
```

<p>Creates new pages. Why aren't the old pages destroyed? Because WP keeps them in a history of pages as to support the back button. Thus, in my case, if I replace one call of <code>NavigationService.Navigate</code> with</p>

```csharp
NavigationService.GoBack();
```

<p>then the old pages get removed from the page history stack and no memory leak occurs. That's a solution if pages follow a clear hierarchical order First Page -> Second Page -> Third Page -> ..., but what if the app is implemented in such as way to all pages can navigate between each other and there is not clear "first" page, <em>ala</em> finite state machine? </p>
<p>Then it becomes important to remove stack frames every time navigation occurs.</p>

```csharp
if (App.RootFrame.CanGoBack)
    App.RootFrame.RemoveBackEntry();
NavigationService.Navigate(...);
```

<p>In practice most apps do follow a hierarchical structure as alternatives are highly likely to break guidelines regarding the use of the back button but if the developer requires strict control over page navigation, then it's important to remove unused stack via <code>RemoveBackEntry</code>.</p>
<p>Garbage collection is nice, but it's no free lunch!</p>
<p><b>In this blog post, I described only one way memory "leaks" can occur. I've added links below to other possible causes, as explained by other writers.</b><br />
<a>http://sartorialsolutions.wordpress.com/2010/10/15/wp7-detecting-memory-leaks/</a><br />
<a>http://suchan.cz/2013/11/how-to-debug-most-common-memory-leaks-on-wp8/</a><br />
<a>http://blogs.codes-sources.com/kookiz/archive/2013/02/17/wpdev-memory-leak-with-bitmapimage.aspx</a><br />
<a>http://blogs.msdn.com/b/tess/archive/2006/01/23/net-memory-leak-case-study-the-event-handlers-that-made-the-memory-baloon.aspx</a></p>
