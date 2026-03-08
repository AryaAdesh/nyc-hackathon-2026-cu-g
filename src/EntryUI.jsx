import { useState, useEffect, useRef } from 'react';

export default function EntryUI({ onSubmit, isListening, setIsListening }) {
    const [prompt, setPrompt] = useState("");
    const [liveTranscript, setLiveTranscript] = useState("");

    const audioContextRef = useRef(null);
    const streamRef = useRef(null);
    const animationFrameRef = useRef(null);
    const dotRefs = useRef([]);
    const recognitionRef = useRef(null);

    useEffect(() => {
        if (isListening) {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (SpeechRecognition) {
                const recognition = new SpeechRecognition();
                recognition.continuous = true;
                recognition.interimResults = true;

                recognition.onresult = (event) => {
                    let currentTranscript = "";
                    for (let i = event.resultIndex; i < event.results.length; i++) {
                        currentTranscript += event.results[i][0].transcript;
                    }
                    setLiveTranscript(currentTranscript);
                };

                recognition.start();
                recognitionRef.current = recognition;
            } else {
                console.warn("Speech recognition not supported in this browser.");
            }

            navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
                streamRef.current = stream;
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                const audioCtx = new AudioContext();
                const analyzer = audioCtx.createAnalyser();
                analyzer.fftSize = 256;
                const source = audioCtx.createMediaStreamSource(stream);
                source.connect(analyzer);
                audioContextRef.current = audioCtx;

                const dataArray = new Uint8Array(analyzer.frequencyBinCount);
                const voiceBins = [2, 5, 10, 18];

                const renderFrame = () => {
                    analyzer.getByteFrequencyData(dataArray);
                    for (let i = 0; i < 4; i++) {
                        if (dotRefs.current[i]) {
                            const rawVolume = dataArray[voiceBins[i]];
                            const normalized = rawVolume / 255;
                            const scaleY = 1 + Math.pow(normalized, 2.5) * 8;
                            dotRefs.current[i].style.transform = `scaleY(${scaleY})`;
                        }
                    }
                    animationFrameRef.current = requestAnimationFrame(renderFrame);
                };
                renderFrame();
            }).catch(err => console.error("Mic access denied:", err));

        } else {
            if (recognitionRef.current) recognitionRef.current.stop();
            if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);
            if (streamRef.current) streamRef.current.getTracks().forEach(track => track.stop());
            if (audioContextRef.current) audioContextRef.current.close();

            dotRefs.current.forEach(dot => {
                if (dot) dot.style.transform = 'scaleY(1)';
            });
            setLiveTranscript(""); // Clear transcript on stop
        }

        return () => {
            if (recognitionRef.current) recognitionRef.current.stop();
            if (animationFrameRef.current) cancelAnimationFrame(animationFrameRef.current);
            if (streamRef.current) streamRef.current.getTracks().forEach(track => track.stop());
        };
    }, [isListening]);

    const handleFinishRecording = () => {
        setIsListening(false);
        const finalPrompt = liveTranscript || prompt;
        if (finalPrompt.trim() !== "") {
            onSubmit(finalPrompt);
        }
    };

    return (
        <div style={{
            position: 'absolute', top: 0, left: 0, width: '100vw', height: '100vh',
            zIndex: 10, pointerEvents: 'none', fontFamily: '"Space Grotesk", sans-serif'
        }}>

            {/* Invisible Overlay to capture taps when listening */}
            {isListening && (
                <div
                    style={{ position: 'absolute', inset: 0, pointerEvents: 'auto', cursor: 'pointer', zIndex: 5 }}
                    onClick={handleFinishRecording}
                />
            )}

            {/* HARD-PINNED TOP: Title */}
            <h1 style={{
                position: 'absolute', top: '15vh', width: '100%', textAlign: 'center', margin: 0,
                color: 'white', fontSize: '20px', fontWeight: '400', letterSpacing: '2px', textTransform: 'uppercase',
                opacity: isListening ? 0 : 1, transition: 'opacity 0.4s ease',
            }}>
                What universe are we building?
            </h1>

            {/* HARD-PINNED MIDDLE-TOP: Live Transcription Text */}
            <div style={{
                position: 'absolute', top: '35vh', width: '100%', textAlign: 'center',
                color: 'white', fontSize: '28px', fontWeight: '400',
                opacity: isListening ? 1 : 0, transition: 'opacity 0.4s ease',
                textShadow: '0 4px 12px rgba(0,0,0,0.5)', zIndex: 10
            }}>
                {liveTranscript || (isListening ? "Listening..." : "")}
            </div>

            {/* HARD-PINNED CENTER: The Waveform */}
            <div style={{
                position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
                display: isListening ? 'flex' : 'none', gap: '24px', alignItems: 'center', height: '80px', zIndex: 10
            }}>
                {[0, 1, 2, 3].map((i) => (
                    <div key={i} ref={el => dotRefs.current[i] = el}
                         style={{
                             width: '24px', height: '24px', backgroundColor: '#ffffff', borderRadius: '50px',
                             boxShadow: '0 0 20px rgba(255,255,255,0.8)', transition: 'transform 0.08s cubic-bezier(0.2, 0.8, 0.2, 1)'
                         }}
                    />
                ))}
            </div>

            {/* HARD-PINNED MIDDLE-BOTTOM: Helper Text */}
            <div style={{
                position: 'absolute', bottom: '25vh', width: '100%', textAlign: 'center',
                color: '#888', fontSize: '14px', letterSpacing: '1px',
                opacity: isListening ? 1 : 0, transition: 'opacity 0.5s ease',
                animation: isListening ? 'pulse 2s infinite' : 'none'
            }}>
                Tap anywhere to generate
            </div>

            {/* HARD-PINNED BOTTOM: Input Pill */}
            <div style={{
                position: 'absolute', bottom: '10vh', left: '50%', transform: 'translateX(-50%)',
                pointerEvents: isListening ? 'none' : 'auto', opacity: isListening ? 0 : 1, transition: 'opacity 0.4s ease',
                display: 'flex', alignItems: 'center', gap: '12px', background: 'rgba(255, 255, 255, 0.05)',
                backdropFilter: 'blur(20px)', WebkitBackdropFilter: 'blur(20px)', border: '1px solid rgba(255, 255, 255, 0.08)',
                borderRadius: '50px', padding: '12px 24px', width: 'min(90%, 400px)', zIndex: 10
            }}>
                <svg
                    onClick={() => setIsListening(true)}
                    width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#a1a1aa" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
                    style={{ cursor: 'pointer', flexShrink: 0 }}
                >
                    <path d="M12 2a3 3 0 0 0-3 3v7a3 3 0 0 0 6 0V5a3 3 0 0 0-3-3z"></path>
                    <path d="M19 10v2a7 7 0 0 1-14 0v-2"></path><line x1="12" y1="19" x2="12" y2="23"></line><line x1="8" y1="23" x2="16" y2="23"></line>
                </svg>
                <input
                    type="text" placeholder="Describe a concept..."
                    value={prompt} onChange={(e) => setPrompt(e.target.value)}
                    onKeyDown={(e) => { if (e.key === 'Enter' && prompt.trim() !== "") onSubmit(prompt); }}
                    style={{ background: 'transparent', border: 'none', color: 'white', fontSize: '16px', width: '100%', outline: 'none', fontFamily: '"Space Grotesk", sans-serif' }}
                />
            </div>

        </div>
    );
}