import wave
from moviepy.editor import concatenate_audioclips, AudioFileClip

#infiles = ["wai.wav", "staf.wav"]
infiles = []
outfile = "records\\recap.wav"
space="records\\my_record.wav" #espace  entre 2 enregistrements




def concatenate_audio_moviepy(audio_clip_paths, output_path):
    """Concatenates several audio files into one audio file using MoviePy
    and save it to `output_path`. Note that extension (mp3, etc.) must be added to `output_path`"""
    clips = [AudioFileClip(c) for c in audio_clip_paths]
    final_clip = concatenate_audioclips(clips)
    final_clip.write_audiofile(output_path)



#concatenate_audio_moviepy(infiles,outfile)

def Add_conv(conv):
    infiles.append(conv)
    infiles.append(space)

def Recap():
    concatenate_audio_moviepy(infiles, outfile)
    print("you can have the summary of this conversation in the audio file "+ outfile)