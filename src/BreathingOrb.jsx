import { useRef } from 'react';
import { useFrame } from '@react-three/fiber';
import { Sphere, MeshDistortMaterial } from '@react-three/drei';
import * as THREE from 'three';

export default function BreathingOrb({ isListening }) {
    const sphereRef = useRef();

    useFrame(({ clock }) => {
        const elapsedTime = clock.getElapsedTime();
        if (sphereRef.current) {
            sphereRef.current.rotation.y = elapsedTime * 0.1;

            // Smoothly shrink the orb to 0 if listening, or back to 1 if not
            const targetScale = isListening ? 0 : 1;
            sphereRef.current.scale.lerp(new THREE.Vector3(targetScale, targetScale, targetScale), 0.1);
        }
    });

    return (
        <group>
            <ambientLight intensity={0.8} />
            <directionalLight position={[2, 5, 2]} intensity={2.5} color="#ffffff" />
            <pointLight position={[-2, -2, 2]} intensity={2} color="#4285f4" />

            {/* Smaller args: [0.8, 64, 64] */}
            <Sphere ref={sphereRef} args={[0.8, 64, 64]} position={[0, 0, 0]}>
                <MeshDistortMaterial
                    color="#f8f9fa"
                    emissive="#2a5699"    // Deeper, quieter glow
                    roughness={0.85}      // High texture, very matte
                    metalness={0.1}
                    distort={0.15}        // Barely breathing, very subtle
                    speed={0.8}           // Slower movement
                    clearcoat={0.2}       // Gives it a slight icy sheen on top of the texture
                />
            </Sphere>
        </group>
    );
}