import { useRef, useMemo, useEffect } from 'react';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

export default function ParticleTransition({ onComplete }) {
    const pointsRef = useRef();

    // Pure side-effect timer. 5 seconds for the transition.
    useEffect(() => {
        const timer = setTimeout(() => {
            if (onComplete) onComplete();
        }, 5000);
        return () => clearTimeout(timer);
    }, [onComplete]);

    // 1. Generate a programmatic glowing circle texture (No external image needed!)
    const glowTexture = useMemo(() => {
        const canvas = document.createElement('canvas');
        canvas.width = 64; canvas.height = 64;
        const context = canvas.getContext('2d');

        // Create a radial gradient from solid white to transparent
        const gradient = context.createRadialGradient(32, 32, 0, 32, 32, 32);
        gradient.addColorStop(0, 'rgba(255, 255, 255, 1)');      // Hot white core
        gradient.addColorStop(0.2, 'rgba(0, 242, 254, 0.8)');    // Gemini cyan mid-ring
        gradient.addColorStop(1, 'rgba(0, 0, 0, 0)');            // Fade to black/transparent

        context.fillStyle = gradient;
        context.fillRect(0, 0, 64, 64);
        return new THREE.CanvasTexture(canvas);
    }, []);

    // 2. Spawn 10,000 particles in a microscopic sphere at the center
    const particleCount = 30000;
    const particlesPosition = useMemo(() => {
        const positions = new Float32Array(particleCount * 3);
        for (let i = 0; i < particleCount; i++) {
            // Spherical math creates a perfect tight cluster
            const radius = Math.random() * 0.2; // Starts very tiny
            const theta = Math.random() * 2 * Math.PI;
            const phi = Math.acos(Math.random() * 2 - 1);

            positions[i * 3] = radius * Math.sin(phi) * Math.cos(theta);     // x
            positions[i * 3 + 1] = radius * Math.sin(phi) * Math.sin(theta); // y
            positions[i * 3 + 2] = radius * Math.cos(phi);                   // z
        }
        return positions;
    }, []);

    useFrame((state) => {
        const time = state.clock.getElapsedTime();
        if (pointsRef.current) {
            // Add a cool twisting rotation to the explosion
            pointsRef.current.rotation.y = time * 0.5;
            pointsRef.current.rotation.z = time * 0.2;

            // 3. Exponential Warp Speed Math
            // It starts at scale 1, and rapidly accelerates outward past the camera
            const scale = 1 + Math.pow(time * 2.5, 3);
            pointsRef.current.scale.set(scale, scale, scale);
        }
    });

    return (
        <points ref={pointsRef}>
            <bufferGeometry>
                <bufferAttribute
                    attach="attributes-position"
                    count={particlesPosition.length / 3}
                    array={particlesPosition}
                    itemSize={3}
                />
            </bufferGeometry>
            <pointsMaterial
                size={0.2}                    // Much larger particles
                map={glowTexture}             // Use our glowing circle
                transparent={true}            // Allow transparency
                opacity={1}
                depthWrite={false}            // IMPORTANT: Stops dark squares from blocking glow
                blending={THREE.AdditiveBlending} // Makes overlapping particles brighter (like light)
                sizeAttenuation={true}        // Get bigger as they hit the camera
            />
        </points>
    );
}