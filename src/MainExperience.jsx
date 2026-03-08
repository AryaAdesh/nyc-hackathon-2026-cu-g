import { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { ScrollControls, useScroll, Html, Text, Stars } from '@react-three/drei';
import * as THREE from 'three';

// --- THE IDEAS ---
const ideas = [
    { id: 1, title: 'Concept Alpha', subtitle: 'Neon Cyberpunk Aesthetics', z: -30, x: -7 },
    { id: 2, title: 'Concept Beta', subtitle: 'Organic Bioluminescence', z: -90, x: 7 },
    { id: 3, title: 'Concept Gamma', subtitle: 'Minimalist High-Fashion', z: -150, x: -7 },
];

// --- INTERACTIVE NODES ---
function IdeaNode({ data, onSelect }) {
    const [hovered, setHovered] = useState(false);
    const meshRef = useRef();

    useFrame(() => {
        if (meshRef.current) {
            meshRef.current.rotation.y += 0.002;
            meshRef.current.position.y = Math.sin(Date.now() / 2000 + data.id) * 0.3;
        }
    });

    const htmlX = data.x < 0 ? 7 : -7;

    return (
        <group position={[data.x, 0, data.z]}>

            <group
                onPointerOver={(e) => { e.stopPropagation(); setHovered(true); document.body.style.cursor = 'pointer'; }}
                onPointerOut={(e) => { e.stopPropagation(); setHovered(false); document.body.style.cursor = 'auto'; }}
                onClick={(e) => { e.stopPropagation(); document.body.style.cursor = 'auto'; onSelect(data.id); }}
            >
                <mesh ref={meshRef} castShadow>
                    <planeGeometry args={[10, 5.6]} />
                    <meshStandardMaterial
                        color="#0a0a0a"
                        emissive={hovered ? "#00f2fe" : "#000000"}
                        emissiveIntensity={0.6}
                        wireframe
                    />
                </mesh>

                <Text position={[0, -3.5, 0]} fontSize={0.3} color={hovered ? "#ffffff" : "#666"} letterSpacing={0.2}>
                    {hovered ? "CLICK TO INITIALIZE WORLD" : `NODE 0${data.id}`}
                </Text>
            </group>

            <Html position={[htmlX, 1, 0]} transform distanceFactor={12}>
                <div style={{
                    background: hovered ? 'rgba(15, 15, 20, 0.9)' : 'rgba(10, 10, 10, 0.6)',
                    backdropFilter: 'blur(24px)', WebkitBackdropFilter: 'blur(24px)',
                    border: hovered ? '1px solid #00f2fe' : '1px solid rgba(255, 255, 255, 0.1)',
                    borderRadius: '16px', padding: '32px', width: '400px',
                    color: '#e0e0e0', fontFamily: '-apple-system, BlinkMacSystemFont, "Inter", sans-serif',
                    transition: 'all 0.4s cubic-bezier(0.2, 0.8, 0.2, 1)', cursor: 'pointer',
                    transform: hovered ? 'scale(1.02)' : 'scale(1)'
                }}
                     onPointerEnter={() => { setHovered(true); document.body.style.cursor = 'pointer'; }}
                     onPointerLeave={() => { setHovered(false); document.body.style.cursor = 'auto'; }}
                     onClick={() => { document.body.style.cursor = 'auto'; onSelect(data.id); }}
                >
                    <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '16px', marginBottom: '20px' }}>
                        <span style={{ fontSize: '11px', letterSpacing: '2px', color: '#888' }}>VEO / NANO</span>
                        <span style={{ fontSize: '11px', letterSpacing: '2px', color: '#00f2fe' }}>READY</span>
                    </div>
                    <h2 style={{ fontSize: '32px', fontWeight: '300', color: 'white', margin: '0 0 12px 0', letterSpacing: '-1px' }}>{data.title}</h2>
                    <p style={{ fontSize: '14px', color: '#aaa', margin: 0, lineHeight: '1.6' }}>{data.subtitle}</p>
                </div>
            </Html>

        </group>
    );
}

// --- THE LOCKED-DOWN CAMERA TUNNEL ---
function ScrollScene({ onNodeSelect }) {
    const scroll = useScroll();

    useFrame((state) => {
        const currentZ = THREE.MathUtils.lerp(10, -180, scroll.offset);
        state.camera.position.z = currentZ;
        state.camera.position.y = 0;
        state.camera.position.x = THREE.MathUtils.lerp(state.camera.position.x, state.mouse.x * 0.5, 0.1);
        state.camera.lookAt(0, 0, currentZ - 50);
    });

    return (
        <group>
            {/* 🚨 REPLACED VIDEO WITH NATIVE 3D STARS 🚨 */}
            {/* This will never hang your browser and looks incredible when moving in Z-space */}
            <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade speed={1} />

            <fog attach="fog" args={['#050505', 20, 70]} />
            <ambientLight intensity={1.2} />
            <directionalLight position={[10, 20, 10]} intensity={2} />

            {ideas.map((nodeData) => (
                <IdeaNode key={nodeData.id} data={nodeData} onSelect={onNodeSelect} />
            ))}
        </group>
    );
}

export default function MainExperience({ onNodeSelect }) {
    return (
        <ScrollControls pages={5} damping={0.2}>
            <ScrollScene onNodeSelect={onNodeSelect} />
        </ScrollControls>
    );
}