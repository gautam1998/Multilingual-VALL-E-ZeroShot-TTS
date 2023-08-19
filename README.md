# Zero-Shot Evaluation of QuickVC in Multilingual Setting

## Developed By: 

### [Gautam Srinidhi Iruvanti](https://www.mccormick.northwestern.edu/artificial-intelligence/people/students/2022-2023/gautam-iruvanti.html)
(gautamiruvanti2024@u.northwestern.edu)
### [Surya Pratap Parmar](https://www.mccormick.northwestern.edu/artificial-intelligence/people/students/2022-2023/surya-parmar.html)
(suryaparmar2024@u.northwestern.edu)
### [Vishal Shrivastava](https://www.mccormick.northwestern.edu/artificial-intelligence/people/students/2022-2023/vishal-shrivastava.html)
(vishalshrivastava2024@u.northwestern.edu)

**********
## Course: [Deep Generative Models, CS 496 Spring 2023, Northwestern University](https://interactiveaudiolab.github.io/teaching/generative_deep_models.html#calendar)

### Professor: [Bryan Pardo](http://bryanpardo.com/)
### TA: [Patrick O’Reilly](https://oreillyp.github.io/)
*********** 

## <b>Background</b>
<p>
It is a commonly accepted fact in the AI community that the Automatic Speech Recognition (ASR) models can exhibit bias towards native speakers due to several factors. In one of the recent studies conducted at Washington University<sup>1</sup>, the researchers tried to examine discriminatory automatic speech recognition (ASR) performance as a function of speakers’ geopolitical orientation, specifically their first language. Unsurprisingly, they found that the ASR models were biased towards the native English speakers. We can see the results in the following graph where the X-axis represents a metric called “Word Information Lost” - the fraction of words that were changed, inserted, or deleted during the speech generation; and the Y-axis shows the first language of the respective speakers. As we can see in the graph, for all the three major ASR services, word information loss is lowest for native English speakers and it gets higher and higher for speakers from different backgrounds.

<span class="img_container center" style="display: block;">
    <img alt="test" src="./images/asr_bias.png?raw=true" style="display:block; margin-left: auto; margin-right: auto;" title="caption" />
    <span class="img_caption" style="display: block; text-align: center;">Figure 1: Mean word information lost (WIL) for ASR services vs. first language<sup>1</sup></span>
</span>
</p>
&nbsp;
&nbsp;
<p>
We believe that one of the primary reasons for this disparity is that the ASR models are typically trained on large amounts of data, which may consist predominantly of speech from native speakers. This happens due to a lack of labeled audio datasets of non-native speakers speaking a particular language. As a result, the ASR models struggle with recognizing and accurately transcribing non-native accents or variations in pronunciation.
This problem motivated us to think about some potential ways of generating high volumes of labeled audio data in multiple languages with diversified accents. Now, of course, we can generate high volumes of labled speech by using a text-to-speech system, but it doesn’t solve the problem of accented speech, which is the main issue with the low performance of ASR systems. Guo et. al<sup>2</sup> have recently introduced QuickVC - an any-to-many voice conversion framework using inverse short-time Fourier transforms. QuickVC is trained on English speech, but we wondered if we can use it for generating accented speech in other languages too. We believed that doing so would provide us with a viable option for generating high volumes of labeled audio data with diversified accents that can be used for training or fine-tuning ASR systems.
<span class="img_container center" style="display: block;">
    <img alt="test" src="./images/initial_flow_design.png?raw=true" style="display:block; margin-left: auto; margin-right: auto;" title="caption" />
    <span class="img_caption" style="display: block; text-align: center;">Figure 2:  Flow design for generating high volume of labeled audio with diversified accents</span>
</span>
</p>
&nbsp;
&nbsp;

## <b>Framework</b>
<p>
Our flow starts with an input text in one of the ten selected languages. We feed this input text to Meta's text-to-speech (TTS) model<sup>6</sup>, which then generates a synthetic audio signal with the given text as the content. This audio signal serves as a source speech to the QuickVC voice conversion model. Then, we use ten different audio samples from the VCTK dataset as the target speech signals and feed them one by one to the QuickVC model along with the source audio to generate new speech signals having the content of the source audio and the style of the target audio. We ran this experiment for ten different languages, each having a hundred different prompts. In total, we generated 10 (languages) * 100 (prompts) * 10 (target speakers) = 10,000 speech signals.
</p> 
<div><br/></div>
<span class="img_container center" style="display: block;">
    <img alt="test" src="./images/framework_flow.png?raw=true" style="display:block; margin-left: auto; margin-right: auto;" title="caption" />
    <span class="img_caption" style="display: block; text-align: center;">Figure 3: Framework</span>
</span>
<div><br/></div>

## <b>Dataset</b>
<p>
For the text-to-speech synthesis, we used Qi et. al’s massively multilingual (60 languages) data set derived from TED Talk transcripts<sup>3</sup>. We chose to work with ten of the most common languages around the world, which includes English, Hindi, Spanish, Portuguese, Turkish, Russian, Swedish, Hungarian, Indonesian, and German. For target audio samples, we chose ten different speakers from the VCTK corpus<sup>4</sup>, which contains recordings of speech from 110 English speakers with diverse accents. 
</p>

## <b>Evaluation</b>
We wanted to evaluate our framework for two different tasks: 
1. How well the model was able to copy the target speaker's voice (Speaker Similarity).
2. How much of the original content was preserved in the generated speech (Word Error Rate).

### <b>Speaker Similarity</b>
<p>
In order to measure the speaker similarity score for each language, we took the target and generated speech pairs and calculated their speaker embeddings with the help of a pre-trained voice encoder<sup>5</sup>. Then, we calculated the cosine similarity between the embedding pairs and finally averaged the score across all such pairs for a particular language. Cosine similarti score ranges from -1 to 1, where:
a. 1 indicates that the vectors are perfectly similar or identical.

b. 0 indicates no similarity between the vectors.

c. -1 indicates that the vectors are perfectly dissimilar or opposite.
</p>

<span class="img_container center" style="display: block;">
    <img alt="test" src="./images/similarity_measure.png?raw=true" style="display:block; margin-left: auto; margin-right: auto;" title="caption" />
    <span class="img_caption" style="display: block; text-align: center;">Figure 4: Speaker Similarity Measure</span>
</span>
<div><br/></div>

### <b>Word Error Rate (WER)</b>
<p>
Since QuickVC was never trained on any other language except for English, we were interested in knowing how well it would preserve the content of the source audio in different languages. So, we decided to calculate the word error rate (WER) for the generated speech. WER is a common metric of the performance of an automatic speech recognition system. This value indicates the percentage of words that were incorrectly predicted. The lower the value, the better the performance of the ASR system with a WER of 0 being a perfect score. To calculate this, we utilized Meta's massively multilingual speech ASR<sup>6</sup> to generate text tokens for the TTS output as well as the QuickVC output, and then we calculated the word error rate between the two sets of text tokens using JiWER<sup>7</sup> - a simple and fast python package to evaluate automatic speech recognition systems.
</p>
<div><br/></div>
<span class="img_container center" style="display: block;">
    <img alt="test" src="./images/wer_vc.png?raw=true" style="display:block; margin-left: auto; margin-right: auto;" title="caption" />
    <span class="img_caption" style="display: block; text-align: center;">Figure 5: Word Error Rate (WER) - Voice Conversion</span>
</span>
<div><br/></div>
<p>
We also calculated the word error rate between the TTS output and the original text prompt to account for the errors introduced by the Meta's TTS system.
</p>
<div><br/></div>
<span class="img_container center" style="display: block;">
    <img alt="test" src="./images/wer_source.png?raw=true" style="display:block; margin-left: auto; margin-right: auto;" title="caption" />
    <span class="img_caption" style="display: block; text-align: center;">Figure 6: Word Error Rate (WER) - Source</span>
</span>
<div><br/></div>
<p>
Our assumption was that the model will perform well for English content, since it was trained only on English speech. But, we also assumed a significantly worse performance for other languages for the same reason. To our surprise, the model performed decently with other languages as well. The scores are discussed further in detail under the Results section.
</p>

<div><br/></div>


## <b>Results</b>

### <b>Speaker Similarity</b>

| Language      | Cosine Similarity Score |
| ----------- | ----------- |
| English      | 0.84       |
| Hindi   | 0.81        |
| Spanish | 0.80 |
| Portuguese | 0.82 |
| Turkish | 0.82 |
| Russian | 0.82 |
| Swedish | 0.82 |
| Hungarian | 0.80 |
| Indonesian | 0.80 |
| German | 0.81 |

<p>
The average cosine similarity score for each of the ten languages is 0.8 or higher, which indicates that the QuickVC model, despite being trained on just English speech, is robust enough to successfully convert the styles of non-English audio samples as well.
</p>

### <b>Word Error Rate</b>

| Language      | WER Source | WER Voice Conversion | 
| ----------- | ----------- | ----------- | 
| English      | 0.370       | 0.185 |
| Hindi | 0.480 | 0.294 |
| Spanish | 0.317 | 0.153 |
| Portuguese | 0.319 | 0.131 |
| Turkish | 0.624 | 0.444 |
| Russian | 1.025 | 0.310 |
| Swedish | 0.434 | 0.289 |
| Hungarian | 0.532 | 0.327 |
| Indonesian | 0.458 | 0.255 |
| German | 0.535 | 0.226 |

We can see that for most of the languages, the word error rate was comparable to English, in fact, it was even lower for Spanish and Portuguese. These results indicate that QuickVC is able to preserve the content of different languages after voice conversion despite not being trained on any of those languages.

## <b>Demo</b>
### Demo 1 (a): English
<figure>
    <figcaption>source audio:</figcaption>
    <audio
        controls
        src="audio/demo_1/eng.wav">
            <a href="audio/demo_1/eng.wav">
                Download audio
            </a>
    </audio>
</figure>    
<figure>
    <figcaption>target speaker:</figcaption>
    <audio
        controls
        src="audio/demo_1/p318_140.wav">
            <a href="audio/demo_1/p318_140.wav">
                Download audio
            </a>
    </audio>
</figure>
    
<figure>
    <figcaption>output:</figcaption>
    <audio
        controls
        src="audio/demo_1/quickVCeng.wav">
            <a href="audio/demo_1/quickVCeng.wav">
                Download audio
            </a>
    </audio>
</figure>

<p></p>
<div><br/></div>

### Demo 1 (b): English (with Hindi target audio)

<figure>
    <figcaption>source audio:</figcaption>
    <audio
        controls
        src="audio/demo_x/source1.wav">
            <a href="audio/demo_x/source1.wav">
                Download audio
            </a>
    </audio>
</figure>    
<figure>
    <figcaption>target speaker:</figcaption>
    <audio
        controls
        src="audio/demo_x/target1.wav">
            <a href="audio/demo_x/target1.wav">
                Download audio
            </a>
    </audio>
</figure>
    
<figure>
    <figcaption>output:</figcaption>
    <audio
        controls
        src="audio/demo_x/demo.wav">
            <a href="audio/demo_x/demo.wav">
                Download audio
            </a>
    </audio>
</figure>

In this case, we used an out-of-distribution target voice (in hindi), which wasn't present in QuickVC's training dataset, so the results aren't as good as the other demos. It looks like the model converted the source audio to one of the training voices which was closer to the target audio.

<p></p>
<div><br/></div>

### Demo 2: Hindi

<figure>
    <figcaption>source audio:</figcaption>
    <audio
        controls
        src="audio/demo_2/hin.wav">
            <a href="audio/demo_2/hin.wav">
                Download audio
            </a>
    </audio>
</figure>    
<figure>
    <figcaption>target speaker:</figcaption>
    <audio
        controls
        src="audio/demo_2/p312_177.wav">
            <a href="audio/demo_2/p312_177.wav">
                Download audio
            </a>
    </audio>
</figure>
    
<figure>
    <figcaption>output:</figcaption>
    <audio
        controls
        src="audio/demo_2/quickVChin.wav">
            <a href="audio/demo_2/quickVChin.wav">
                Download audio
            </a>
    </audio>
</figure>

<p></p>
<div><br/></div>

### Demo 3: Spanish
<figure>
    <figcaption>source audio:</figcaption>
    <audio
        controls
        src="audio/demo_3/spa.wav">
            <a href="audio/demo_3/spa.wav">
                Download audio
            </a>
    </audio>
</figure>    
<figure>
    <figcaption>target speaker:</figcaption>
    <audio
        controls
        src="audio/demo_3/p374_004.wav">
            <a href="audio/demo_3/p374_004.wav">
                Download audio
            </a>
    </audio>
</figure>
    
<figure>
    <figcaption>output:</figcaption>
    <audio
        controls
        src="audio/demo_3/quickVCspa.wav">
            <a href="audio/demo_3/quickVCspa.wav">
                Download audio
            </a>
    </audio>
</figure>
<p></p>
<div><br/></div>

### Demo 4: Portuguese

<figure>
    <figcaption>source audio:</figcaption>
    <audio
        controls
        src="audio/demo_4/por.wav">
            <a href="audio/demo_4/por.wav">
                Download audio
            </a>
    </audio>
</figure>    
<figure>
    <figcaption>target speaker:</figcaption>
    <audio
        controls
        src="audio/demo_4/p252_003.wav">
            <a href="audio/demo_4/p252_003.wav">
                Download audio
            </a>
    </audio>
</figure>
    
<figure>
    <figcaption>output:</figcaption>
    <audio
        controls
        src="audio/demo_4/quickVCpor.wav">
            <a href="audio/demo_4/quickVCpor.wav">
                Download audio
            </a>
    </audio>
</figure>

<p></p>
<div><br/></div>

### Demo 5: Turkish

<figure>
    <figcaption>source audio:</figcaption>
    <audio
        controls
        src="audio/demo_5/tur.wav">
            <a href="audio/demo_5/tur.wav">
                Download audio
            </a>
    </audio>
</figure>    
<figure>
    <figcaption>target speaker:</figcaption>
    <audio
        controls
        src="audio/demo_5/p225_001.wav">
            <a href="audio/demo_5/p225_001.wav">
                Download audio
            </a>
    </audio>
</figure>
    
<figure>
    <figcaption>output:</figcaption>
    <audio
        controls
        src="audio/demo_5/quickVCtur.wav">
            <a href="audio/demo_5/quickVCtur.wav">
                Download audio
            </a>
    </audio>
</figure>

<p></p>
<div><br/></div>

### Demo 6: Russian

<figure>
    <figcaption>source audio:</figcaption>
    <audio
        controls
        src="audio/demo_6/rus.wav">
            <a href="audio/demo_6/rus.wav">
                Download audio
            </a>
    </audio>
</figure>    
<figure>
    <figcaption>target speaker:</figcaption>
    <audio
        controls
        src="audio/demo_6/p226_005.wav">
            <a href="audio/demo_6/p226_005.wav">
                Download audio
            </a>
    </audio>
</figure>
    
<figure>
    <figcaption>output:</figcaption>
    <audio
        controls
        src="audio/demo_6/quickVCrus.wav">
            <a href="audio/demo_6/quickVCrus.wav">
                Download audio
            </a>
    </audio>
</figure>

<p></p>
<div><br/></div>

### Demo 7: Swedish

<figure>
    <figcaption>source audio:</figcaption>
    <audio
        controls
        src="audio/demo_7/swe.wav">
            <a href="audio/demo_7/swe.wav">
                Download audio
            </a>
    </audio>
</figure>    
<figure>
    <figcaption>target speaker:</figcaption>
    <audio
        controls
        src="audio/demo_7/p229_003.wav">
            <a href="audio/demo_7/p229_003.wav">
                Download audio
            </a>
    </audio>
</figure>
    
<figure>
    <figcaption>output:</figcaption>
    <audio
        controls
        src="audio/demo_7/quickVCswe.wav">
            <a href="audio/demo_7/quickVCswe.wav">
                Download audio
            </a>
    </audio>
</figure>

<p></p>
<div><br/></div>

### Demo 8: Hungarian

<figure>
    <figcaption>source audio:</figcaption>
    <audio
        controls
        src="audio/demo_8/hun.wav">
            <a href="audio/demo_8/hun.wav">
                Download audio
            </a>
    </audio>
</figure>    
<figure>
    <figcaption>target speaker:</figcaption>
    <audio
        controls
        src="audio/demo_8/p246_198.wav">
            <a href="audio/demo_8/p246_198.wav">
                Download audio
            </a>
    </audio>
</figure>
    
<figure>
    <figcaption>output:</figcaption>
    <audio
        controls
        src="audio/demo_8/quickVChun.wav">
            <a href="audio/demo_8/quickVChun.wav">
                Download audio
            </a>
    </audio>
</figure>

<p></p>
<div><br/></div>

### Demo 9: Indonesian

<figure>
    <figcaption>source audio:</figcaption>
    <audio
        controls
        src="audio/demo_9/ind.wav">
            <a href="audio/demo_9/ind.wav">
                Download audio
            </a>
    </audio>
</figure>    
<figure>
    <figcaption>target speaker:</figcaption>
    <audio
        controls
        src="audio/demo_9/p334_304.wav">
            <a href="audio/demo_9/p334_304.wav">
                Download audio
            </a>
    </audio>
</figure>
    
<figure>
    <figcaption>output:</figcaption>
    <audio
        controls
        src="audio/demo_9/quickVCind.wav">
            <a href="audio/demo_9/quickVCind.wav">
                Download audio
            </a>
    </audio>
</figure>

<p></p>
<div><br/></div>

### Demo 10: German

<figure>
    <figcaption>source audio:</figcaption>
    <audio
        controls
        src="audio/demo_10/deu.wav">
            <a href="audio/demo_10/deu.wav">
                Download audio
            </a>
    </audio>
</figure>    
<figure>
    <figcaption>target speaker:</figcaption>
    <audio
        controls
        src="audio/demo_10/p351_003.wav">
            <a href="audio/demo_10/p351_003.wav">
                Download audio
            </a>
    </audio>
</figure>
    
<figure>
    <figcaption>output:</figcaption>
    <audio
        controls
        src="audio/demo_10/quickVCdeu.wav">
            <a href="audio/demo_10/quickVdeu.wav">
                Download audio
            </a>
    </audio>
</figure>

<p></p>
<div><br/></div>

## <b>References</b>
1. https://doi.org/10.48550/arXiv.2208.01157 
2. Guo, Houjian, et al. "QuickVC: Many-to-any Voice Conversion Using Inverse Short-time Fourier Transform for Faster Conversion." arXiv preprint arXiv:2302.08296 (2023). 
3. Ye Qi, Devendra Sachan, Matthieu Felix, Sarguna Padmanabhan, and Graham Neubig. 2018. When and Why Are Pre-Trained Word Embeddings Useful for Neural Machine Translation?. In Proceedings of the 2018 Conference of the North American Chapter of the Association for Computational Linguistics: Human Language Technologies, Volume 2 (Short Papers), pages 529–535, New Orleans, Louisiana. Association for Computational Linguistics.
4. Yamagishi, Junichi; Veaux, Christophe; MacDonald, Kirsten. (2019). CSTR VCTK Corpus: English Multi-speaker Corpus for CSTR Voice Cloning Toolkit (version 0.92), [sound]. University of Edinburgh. The Centre for Speech Technology Research (CSTR). https://doi.org/10.7488/ds/2645.
5. https://github.com/resemble-ai/Resemblyzer
6. https://github.com/facebookresearch/fairseq/tree/main/examples/mms
7. https://github.com/jitsi/jiwer/tree/master








