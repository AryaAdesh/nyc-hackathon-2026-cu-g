import { useState, Suspense } from 'react';
import { Canvas } from '@react-three/fiber';
import { Html } from '@react-three/drei';
import BreathingOrb from './BreathingOrb';
import EntryUI from './EntryUI';
import ParticleTransition from './ParticleTransition';
import LoadingUI from './LoadingUI';
import MainExperience from './MainExperience';

export default function App() {
    const [appState, setAppState] = useState('ENTRY');
    const [isListening, setIsListening] = useState(false);
    const [selectedWorld, setSelectedWorld] = useState(null);

    // 1. Initial Submit
    const handlePromptSubmit = (userPrompt) => {
        setAppState('GENERATING');
    };

    // 2. First Loading Complete
    const handleLoadingComplete = () => {
        setAppState('EXPERIENCE');
    };

    // 3. User Clicks a Node in the Tunnel
    const handleNodeClick = (nodeId) => {
        console.log("User selected world:", nodeId);
        setSelectedWorld(nodeId);
        setAppState('GENERATING_WORLD'); // Trigger the explosion again!
    };

    // 4. Second Loading Complete (Transitioning to the clicked world)
    const handleWorldLoadingComplete = () => {
        setAppState('EXPLORE_WORLD');
    };

    return (
        <div style={{ width: '100vw', height: '100vh', background: '#050505', overflow: 'hidden' }}>

            <Canvas camera={{ position: [0, 0, 5], fov: 45 }}>
                {appState === 'ENTRY' && <BreathingOrb isListening={isListening} />}

                {/* The First Explosion */}
                {appState === 'GENERATING' && <ParticleTransition onComplete={handleLoadingComplete} />}

                {appState === 'EXPERIENCE' && (
                    <Suspense fallback={<Html center><h2 style={{color: 'white', fontFamily: 'sans-serif'}}>Loading Environment...</h2></Html>}>
                        <MainExperience onNodeSelect={handleNodeClick} />
                    </Suspense>
                )}

                {/* The Second Explosion (Triggered by clicking a node) */}
                {appState === 'GENERATING_WORLD' && <ParticleTransition onComplete={handleWorldLoadingComplete} />}

                {appState === 'EXPLORE_WORLD' && (
                    <Html center>
                        <div style={{ textAlign: 'center', color: 'white', fontFamily: '"Space Grotesk", sans-serif' }}>
                            <h1 style={{ fontSize: '48px', fontWeight: '300' }}>World 0{selectedWorld}</h1>
                            <p style={{ color: '#00f2fe' }}>Nano Banana 3D Environment Initialized.</p>
                        </div>
                    </Html>
                )}
            </Canvas>

            {appState === 'ENTRY' && <EntryUI onSubmit={handlePromptSubmit} isListening={isListening} setIsListening={setIsListening} />}
            {(appState === 'GENERATING' || appState === 'GENERATING_WORLD') && <LoadingUI />}

        </div>
    );
}