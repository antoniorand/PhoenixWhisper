$(function() {
  var CONST_SHOW_TRANSCRIPT_CLASS = 'show-transcript';
  var $btnToggleTranscript = $('.btn-toggle-transcript');
  var $mediaLibrary = $('.media-library');
  var $mediaLibraryItemBtn = $('.media-library-item-btn');
  var $activityMediaAudio = $('.activity.media.audio');
  var $activityMediaVideo = $('.activity.media.video');
  var ua = navigator.userAgent.toLowerCase();
  var browserClass = '';
  var $allAudioAndVideoElements = $('audio, video');
    
    
  $mediaLibrary.each(function() {
      $(this).find('.media-library-item-btn').first().addClass('active');
  });
  $mediaLibraryItemBtn.click(function() {
      var $activityMedia = $(this).closest('.activity.media');
      if ($activityMedia.hasClass('video')) {
          loadVideo($(this), true);
      } else if ($activityMedia.hasClass('audio')) {
          loadAudio($(this), true);
      }
  });

    
  $allAudioAndVideoElements.each(function() {
      $(this).on('play', function() {
          $allAudioAndVideoElements.not(this).each(function() {
              $(this)[0].pause();
          });
      });
  });
  
    
  if (ua.indexOf('chrome') > -1) {
      browserClass = 'chrome';
  } else if (ua.indexOf('safari') > -1) {
      browserClass = 'safari';
  } else if (ua.indexOf('firefox') > -1) {
      browserClass = 'firefox';
  }
    
    
  $activityMediaAudio.each(function() {
      var $activityWrapper = $(this);
      var $audio = $activityWrapper.find('audio');
      var $tracks = $audio.find('track');
      var $audioToolbar = $activityWrapper.find('.audio-toolbar');
      var $btnToggleTranscript = $audioToolbar.find('.btn-toggle-transcript');
      var $mediaLibrary = $activityWrapper.find('.media-library');
      var $mediaLibraryItemBtn = $mediaLibrary.find('.media-library-item-btn');
      
      var $firstVideoLibraryBtn = $mediaLibraryItemBtn.first();
      loadAudio($firstVideoLibraryBtn, false);
      
      if ($mediaLibraryItemBtn.length >= 2) {
        $mediaLibrary.removeClass('hide-on-load');
      }
      
      $audioToolbar.addClass(browserClass);
      
      var hasTranscript = false;
      if ($audio.data('transcriptSrc')) {
        hasTranscript = true;
      }
      if (hasTranscript) {
          if ($activityWrapper.data('showTranscriptAtStart')) {
              $activityWrapper.addClass(CONST_SHOW_TRANSCRIPT_CLASS);
              $audio.addClass(CONST_SHOW_TRANSCRIPT_CLASS);
              $btnToggleTranscript.text('Hide transcript');
          }
      } else {
          $btnToggleTranscript.hide();
      }

      if ($audioToolbar.children(':visible').length === 0) {
          $audioToolbar.hide();
      }
      
      $audio.on('pause seeking', function(evt) {
          var str = msToTimecode(evt.target.currentTime*1000);
          console.log(str);
      });
      $audio.on('timeupdate', function(evt) {
          var $audio = $(this);
          if ($audio.hasClass(CONST_SHOW_TRANSCRIPT_CLASS)) {
              var secs = evt.target.currentTime;
              var timecode = msToTimecode(secs*1000);
              var $activityWrapper = $audio.closest('.activity.media.audio');
              var $transcriptWrapper = $activityWrapper.find('.transcript-wrapper');
              var $cuePoints = $transcriptWrapper.find('.cuepoint');
              $cuePoints.removeClass('active');
              var $cuepoint, $activeCuepoint;
              $cuePoints.each(function(index) {
                  $cuepoint = $(this);
                  var startTime = $cuepoint.data('startTime');
                  var endTime = $cuepoint.data('endTime');
                  if (secs >= startTime && secs < endTime) {
                      $activeCuepoint = $cuepoint;
                      $activeCuepoint.addClass('active');
                      return false; 
                  }
              });
              // if ($activeCuepoint) {
              //     console.log($activeCuepoint);
              // }
          }
      });
  });
    
    
  $activityMediaVideo.each(function() {
      var $activityWrapper = $(this);
      var $video = $activityWrapper.find('video');
      var $tracks = $video.find('track');
      var $videoToolbar = $activityWrapper.find('.video-toolbar');
      var $btnToggleTranscript  = $videoToolbar.find('.btn-toggle-transcript');
      var $mediaLibrary = $activityWrapper.find('.media-library');
      var $mediaLibraryItemBtn = $mediaLibrary.find('.media-library-item-btn');
      
      var $firstVideoLibraryBtn = $mediaLibraryItemBtn.first();
      loadVideo($firstVideoLibraryBtn, false);

      if ($mediaLibraryItemBtn.length >= 2) {
        $mediaLibrary.removeClass('hide-on-load');
      }
      
      $videoToolbar.addClass(browserClass);
      
      $video.click(function() {
          var video = $(this)[0];
          if (video.paused) {
              video.play();
          } else {
              video.pause();
          }
      });
      
      var hasTranscript = false;
      $mediaLibraryItemBtn.each(function() {
          var $btn = $(this);
          if ( $btn.data('transcriptSrc')) {
              hasTranscript = true;
              return false;
          }
      });
      
      if (hasTranscript) {
          if ($activityWrapper.data('showTranscriptAtStart')) {
              $activityWrapper.addClass(CONST_SHOW_TRANSCRIPT_CLASS);
              $video.addClass(CONST_SHOW_TRANSCRIPT_CLASS);
              $btnToggleTranscript.text('Hide transcript');
          }
      } else {
          $btnToggleTranscript.hide();
      }
      
      if ($videoToolbar.children(':visible').length === 0) {
          $videoToolbar.hide();
      }

      $video.on('pause seeking', function(evt) {
          var str = msToTimecode(evt.target.currentTime*1000);
          console.log(str);
      });
      $video.on('timeupdate', function(evt) {
          var $video = $(this);
          if ($video.hasClass(CONST_SHOW_TRANSCRIPT_CLASS)) {
              var secs = evt.target.currentTime;
              var timecode = msToTimecode(secs*1000);
              var $videoAndTranscriptWrapper = $video.closest('.video-and-transcript-wrapper');
              var $cuePoints = $videoAndTranscriptWrapper.find('.cuepoint');
              $cuePoints.removeClass('active');
              var $cuepoint, $activeCuepoint;
              $cuePoints.each(function(index) {
                  $cuepoint = $(this);
                  var startTime = $cuepoint.data('startTime');
                  var endTime = $cuepoint.data('endTime');
                  if (secs >= startTime && secs < endTime) {
                      $activeCuepoint = $cuepoint;
                      $activeCuepoint.addClass('active');
                      return false; 
                  }
              });
              // if ($activeCuepoint) {
              //     console.log($activeCuepoint);
              // }
          }
      });
      
      var numTracks = $video[0].textTracks.length;
      for (var i = 0; i < numTracks; i++) {
          if ($video[0].textTracks[i].kind === 'chapters') {
              $video[0].textTracks[i].mode = 'showing';
          } else if ($video[0].textTracks[i].kind === 'captions') {
              $video[0].textTracks[i].mode = 'hidden';  
          }
      }
      $video.attr('data-showing-captions', 'false');

      var $captionsTrack = $video.find('track[kind="captions"]');
      $captionsTrack.on('load', function(evt) {
          var $activityMedia = $(this).closest('.activity.media.video');
          showCaptionsOnLoadIfPreviouslyShowing($activityMedia);
          setChaptersTrackModeToHidden($activityMedia);
      });
      
      var $chaptersTrack = $video.find('track[kind="chapters"]');
      $chaptersTrack.on('load', function(evt) {
          var $activityMedia = $(this).closest('.activity.media.video');
          createInteractiveTranscriptFromChapterVTT($activityMedia);
      });
  });
  
    
  $btnToggleTranscript.click(function() {
      var $toggleTranscriptBtn = $(this);
      var $activityWrapper = $toggleTranscriptBtn.closest('.activity-wrapper.media');
      var $nextSibling = $toggleTranscriptBtn.next();
      var $video = $activityWrapper.find('video');
      $activityWrapper.toggleClass(CONST_SHOW_TRANSCRIPT_CLASS);
      $video.toggleClass(CONST_SHOW_TRANSCRIPT_CLASS);
      if ($video.hasClass(CONST_SHOW_TRANSCRIPT_CLASS)) {
          $toggleTranscriptBtn.text('Hide transcript');
      } else {
          $toggleTranscriptBtn.text('Show transcript');
      }
  });
  
    
  function loadAudio($btn, triggeredByClick) {
      console.log('loadAudio()');
      var $item = $btn;
      var $activityWrapper = $item.closest('.activity.media.audio');
      var $audio = $activityWrapper.find('audio');
      var audioSrc = $item.data('audioSrc');
      var $transcriptInner = $activityWrapper.find('.transcript-inner');
      var transcriptSrc = $item.data('transcriptSrc');
      $item.closest('.media-library').find('.media-library-item-btn').removeClass('active');
      $item.addClass('active');
      
      console.log('transcriptSrc: ', transcriptSrc);
      
      $audio.find('source').attr('src', audioSrc);
      $audio[0].load();
      
      if ($audio.data('autoplayOnSelect') && triggeredByClick) {
        $audio[0].play();
      }
      
      $transcriptInner.html('');
      
      if (transcriptSrc) {
          var transcriptFileExtension = getExtensionFromUrl(transcriptSrc);

          if (transcriptFileExtension === 'vtt') {
              $audio.find('track[kind="chapters"]').remove();
              $audio.append('<track kind="chapters" src="'+transcriptSrc+'" default>');
              var $chaptersTrack = $audio.find('track[kind="chapters"]');
              $chaptersTrack.on('load', function(evt) {
                  var $activityMedia = $(this).closest('.activity.media.audio');
                  createInteractiveTranscriptFromChapterVTT($activityMedia);
              });
          } else if (transcriptFileExtension === 'txt') {
              $.ajax({
                  url : transcriptSrc,
                  dataType: "text",
                  success : function (data) {
                      data = data.replace(/^(\n{2,})/gm, '\n');
                      data = data.replace(/\n/g, '<br/>');
                      let array = data.split('<br/><br/>');
                      array = array.map(function(line) {
                          return '<p>' + line + '</p>\n';
                      });
                      data = array.join('\n');
                      $transcriptInner.html(data);
                      $transcriptInner.scrollTop(0);
                  }
              });
          }
      }
  }


  function loadVideo($btn, triggeredByClick) {
      var showingCaptions = undefined;
      var $item = $btn;
      var $activityWrapper = $item.closest('.activity.media.video');
      var $video = $activityWrapper.find('video');
      var numTracks = $video[0].textTracks.length;
      var $transcriptInner = $activityWrapper.find('.transcript-inner');
      var videoSrc = $item.data('videoSrc');
      var captionsSrc = $item.data('captionsSrc');
      var captionsLang = $item.data('captionsLang');
      var captionsLabel = $item.data('captionsLabel');
      var posterSrc = $item.data('posterSrc');
      var transcriptSrc = $item.data('transcriptSrc');
      $item.closest('.media-library').find('.media-library-item-btn').removeClass('active');
      $item.addClass('active');
      
      for (var i = 0; i < numTracks; i++) {
          if ($video[0].textTracks[i].kind === 'captions') {
              if ($video[0].textTracks[i].mode === 'showing') {
                  showingCaptions = true;
                  $video.attr('data-showing-captions', 'true');
              } else {
                  showingCaptions = false;
                  $video.attr('data-showing-captions', 'false');
              }
              $video[0].textTracks[i].mode = 'hidden'; 
          } else if ($video[0].textTracks[i].kind === 'chapters') {
              $video[0].textTracks[i].mode = 'hidden';
          }
      }
      
      $video.find('source').attr('src', videoSrc);
      
      $video.find('track[kind="captions"]').remove();
      $video.append('<track kind="captions" src="'+captionsSrc+'" srclang="'+captionsLang+'" label="'+captionsLabel+'">');
      var $captionsTrack = $video.find('track[kind="captions"]');
      $captionsTrack.on('load', function(evt) {
          var $activityMedia = $(this).closest('.activity.media.video');
          showCaptionsOnLoadIfPreviouslyShowing($activityMedia);
          setChaptersTrackModeToHidden($activityMedia);
      });
      
      $video[0].load();
      if ($video.data('autoplayOnSelect') && triggeredByClick) {
        $video.attr('poster', '');
        $video[0].play();
      } else {
        $video.attr('poster', posterSrc);
      }
      
      var numTracks = $video[0].textTracks.length;
      for (var i = 0; i < numTracks; i++) {
          if ($video[0].textTracks[i].kind === 'chapters') {
              $video[0].textTracks[i].mode = 'showing';
          } else if ($video[0].textTracks[i].kind === 'captions') {
              $video[0].textTracks[i].mode = 'hidden';
          }
      }
      
      $transcriptInner.html('');
      
      if (transcriptSrc) {
          var transcriptFileExtension = getExtensionFromUrl(transcriptSrc);

          if (transcriptFileExtension === 'vtt') {
              $video.find('track[kind="chapters"]').remove();
              $video.append('<track kind="chapters" src="'+transcriptSrc+'" default>');
              var $chaptersTrack = $video.find('track[kind="chapters"]');
              $chaptersTrack.on('load', function(evt) {
                  var $activityMedia = $(this).closest('.activity.media.video');
                  createInteractiveTranscriptFromChapterVTT($activityMedia);
              });
          } else if (transcriptFileExtension === 'txt') {
              $.ajax({
                  url : transcriptSrc,
                  dataType: "text",
                  success : function (data) {
                      data = data.replace(/^(\n{2,})/gm, '\n');
                      data = data.replace(/\n/g, '<br/>');
                      let array = data.split('<br/><br/>');
                      array = array.map(function(line) {
                          return '<p>' + line + '</p>\n';
                      });
                      data = array.join('\n');
                      $transcriptInner.html(data);
                      $transcriptInner.scrollTop(0);
                  }
              });
          }
      }
  }
    
    
  function getExtensionFromUrl(url) {
      var extension = '';
      var pattern = /\.([0-9a-z]+)(?:[\?#]|$)/i;
      if (url.match(pattern) && url.match(pattern)[1]) {
          extension = url.match(pattern)[1];
      }
      return extension;
  }
  
  
  function showCaptionsOnLoadIfPreviouslyShowing($activityMedia) {
      var $audioOrVideoElement;
      if ($activityMedia.hasClass('video')) {
          $audioOrVideoElement  = $activityMedia.find('video');
      } else if ($activityMedia.hasClass('audio')) {
          $audioOrVideoElement  = $activityMedia.find('audio');   
      } else {
          return false;
      }
      if ($audioOrVideoElement.attr('data-showing-captions') === 'true') {
          var numTracks = $audioOrVideoElement[0].textTracks.length;
          for (var i = 0; i < numTracks; i++) {
              if ($audioOrVideoElement[0].textTracks[i].kind === 'captions') {
                  $audioOrVideoElement[0].textTracks[i].mode = 'showing';
              }
          }
      }
  }
  
  
  function setChaptersTrackModeToHidden($activityMedia) {
      var $audioOrVideoElement;
      if ($activityMedia.hasClass('video')) {
          $audioOrVideoElement  = $activityMedia.find('video');
      } else if ($activityMedia.hasClass('audio')) {
          $audioOrVideoElement  = $activityMedia.find('audio');   
      } else {
          return false;
      }
      var numTracks = $audioOrVideoElement[0].textTracks.length;
      for (var i = 0; i < numTracks; i++) {
          if ($audioOrVideoElement[0].textTracks[i].kind === 'chapters') {
              $audioOrVideoElement[0].textTracks[i].mode = 'hidden';
          }
      }
  }
  
  
  function createInteractiveTranscriptFromChapterVTT($activityMedia) {
      var $audioOrVideoElement;
      if ($activityMedia.hasClass('video')) {
          $audioOrVideoElement  = $activityMedia.find('video');
      } else if ($activityMedia.hasClass('audio')) {
          $audioOrVideoElement  = $activityMedia.find('audio');   
      } else {
          return false;
      }
      var $transcriptInner = $activityMedia.find('.transcript-inner');
      var transcriptHtml = '';
      var textTracks = $audioOrVideoElement[0].textTracks;
      var numTracks = textTracks.length;
      var chaptersTrack = undefined;
      for (var i=0; i<numTracks; i++) {
          if (textTracks[i].kind === 'chapters') {
              chaptersTrack = textTracks[i];
          }
      }
      if (chaptersTrack) {
        chaptersTrack.mode = 'showing';
        var cues = chaptersTrack.cues;
        for (var i=0; i<cues.length; i++) {
            transcriptHtml += '<p role="button" tabindex="0" class="cuepoint" data-id="'+cues[i].id+'" data-start-time="'+cues[i].startTime+'" data-end-time="'+cues[i].endTime+'">' + cues[i].text + '</p>';
        }
        $transcriptInner.html(transcriptHtml);
        var $cuepoints = $transcriptInner.find('.cuepoint');
        $cuepoints.click(function() {
            console.log('Cuepoint clicked')
            var $cuepoint = $(this);
            var $activityMedia = $cuepoint.closest('.activity.media');
            var $transcriptInner = $activityMedia.find('.transcript-inner');
            var $audioOrVideoElement;
            if ($activityMedia.hasClass('video')) {
                $audioOrVideoElement  = $activityMedia.find('video');
            } else if ($activityMedia.hasClass('audio')) {
                $audioOrVideoElement  = $activityMedia.find('audio');   
            } else {
                return false;
            }
            console.log('$audioOrVideoElement: ', $audioOrVideoElement);
            var $cuepoints = $transcriptInner.find('.cuepoint');
            $audioOrVideoElement[0].currentTime = $cuepoint.data('startTime');
            $cuepoints.each(function() {
                $(this).removeClass('active');
            });
            $cuepoint.addClass('active');
        });
      } else {
        console.log('No chapters track');
      }
  }
  
  
  function msToTimecode(durationInMs) {
      var milliseconds = parseInt((durationInMs%1000))
          , seconds = parseInt((durationInMs/1000)%60)
          , minutes = parseInt((durationInMs/(1000*60))%60)
          , hours = parseInt((durationInMs/(1000*60*60))%24);

      hours = (hours < 10) ? "0" + hours : hours;
      minutes = (minutes < 10) ? "0" + minutes : minutes;
      seconds = (seconds < 10) ? "0" + seconds : seconds;
      if (milliseconds < 10) {
          milliseconds = '00' + milliseconds;
      } else if (milliseconds < 100) {
          milliseconds = '0' + milliseconds;
      }
      return hours + ":" + minutes + ":" + seconds + "." + milliseconds;
  }
    
});