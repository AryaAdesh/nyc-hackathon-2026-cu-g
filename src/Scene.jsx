import { useScroll, Html } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';
import { useRef } from 'react';

// Dummy state representing what Gemini will eventually generate
const campaignNodes = [
    { id: 1, title: "The Genesis", z: 0, text: "Ocean plastic sneakers." },
    { id: 2, title: "Cyberpunk Edge", z: -15, text: "Neon, wet asphalt, high energy." },
    { id: 3, title: "Eco-Minimalist", z: -30, text: "Clean lines, natural tones, breathability." },
    { id: 4, title: "High-Fashion", z: -45, text: "Stark studio lighting, dramatic angles." }
];

export default function Scene() {
    const groupRef = useRef();
    const scrollData = useScroll();

    // useFrame runs 60 times a second. We tie the camera/group Z position to the scroll bar.
    useFrame(() => {
        // scrollData.offset goes from 0 to 1 as you scroll down the page
        // We move the entire group towards the camera (positive Z) to simulate flying forward
        const scrollProgress = scrollData.offset;
        const maxZDistance = 45; // The Z-distance of our furthest node

        groupRef.current.position.z = scrollProgress * maxZDistance;
    });

    return (
        <group ref={groupRef}>
            {campaignNodes.map((node) => (
                <group key={node.id} position={[0, 0, node.z]}>

                    {/* A simple glowing 3D sphere to anchor the UI */}
                    <mesh position={[-2, 0, 0]}>
                        <sphereGeometry args={[0.5, 32, 32]} />
                        <meshStandardMaterial color="#00ffcc" emissive="#00ffcc" emissiveIntensity={0.5} />
                    </mesh>

                    {/* The HTML UI pinned to the 3D space */}
                    <Html position={[0, 0, 0]} transform distanceFactor={10}>
                        <div style={{
                            background: 'rgba(255, 255, 255, 0.05)',
                            backdropFilter: 'blur(10px)',
                            border: '1px solid rgba(255, 255, 255, 0.1)',
                            padding: '2rem',
                            borderRadius: '16px',
                            color: 'white',
                            width: '400px',
                            pointerEvents: 'none' // Ensures the 3D scroll doesn't get blocked by the div
                        }}>
                            <h2 style={{ margin: '0 0 10px 0', fontSize: '2rem' }}>{node.title}</h2>
                            <p style={{ margin: 0, opacity: 0.8 }}>{node.text}</p>
                        </div>
                    </Html>

                </group>
            ))}
        </group>
    );
}