'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, X, Shield } from 'lucide-react';

const navLinks = [
    { href: '/', label: 'Home' },
    { href: '/analyze', label: 'Analyze' },
    { href: '/batch', label: 'Batch' },
    { href: '/compare', label: 'Compare' },
    { href: '/reports', label: 'Reports' },
    { href: '/docs', label: 'Docs' },
];

export default function Navigation() {
    const pathname = usePathname();
    const [isScrolled, setIsScrolled] = useState(false);
    const [mobileOpen, setMobileOpen] = useState(false);

    useEffect(() => {
        const handleScroll = () => {
            setIsScrolled(window.scrollY > 20);
        };
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);

    return (
        <>
            <motion.nav
                initial={{ y: -100 }}
                animate={{ y: 0 }}
                transition={{ duration: 0.5, ease: 'easeOut' }}
                style={{
                    position: 'fixed',
                    top: 0,
                    left: 0,
                    right: 0,
                    zIndex: 50,
                    transition: 'all 0.3s ease',
                    backgroundColor: isScrolled ? 'rgba(0,0,0,0.9)' : 'transparent',
                    backdropFilter: isScrolled ? 'blur(12px)' : 'none',
                    borderBottom: isScrolled ? '1px solid rgba(255,255,255,0.1)' : 'none'
                }}
            >
                <div style={{
                    maxWidth: 1200,
                    margin: '0 auto',
                    padding: '0 24px'
                }}>
                    <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'space-between',
                        height: 64
                    }}>
                        {/* Logo */}
                        <Link href="/" style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
                            <motion.div
                                whileHover={{ rotate: 180 }}
                                transition={{ duration: 0.3 }}
                                style={{
                                    width: 32,
                                    height: 32,
                                    border: '1px solid rgba(255,255,255,0.3)',
                                    borderRadius: 8,
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center'
                                }}
                            >
                                <Shield style={{ width: 16, height: 16, color: '#fff' }} />
                            </motion.div>
                            <span style={{
                                color: '#fff',
                                fontWeight: 600,
                                fontSize: 18,
                                letterSpacing: '-0.01em'
                            }}>
                                DeepTrust
                            </span>
                        </Link>

                        {/* Desktop Nav */}
                        <div style={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: 4
                        }} className="desktop-nav">
                            {navLinks.map((link) => (
                                <Link
                                    key={link.href}
                                    href={link.href}
                                    style={{
                                        position: 'relative',
                                        padding: '8px 16px',
                                        fontSize: 14,
                                        fontWeight: 500,
                                        color: pathname === link.href ? '#fff' : 'rgba(255,255,255,0.6)',
                                        transition: 'color 0.2s ease'
                                    }}
                                >
                                    {link.label}
                                    {pathname === link.href && (
                                        <motion.div
                                            layoutId="nav-indicator"
                                            style={{
                                                position: 'absolute',
                                                bottom: 0,
                                                left: 16,
                                                right: 16,
                                                height: 2,
                                                backgroundColor: '#fff',
                                                borderRadius: 1
                                            }}
                                            transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                                        />
                                    )}
                                </Link>
                            ))}
                        </div>

                        {/* CTA Button */}
                        <div className="desktop-cta">
                            <Link
                                href="/analyze"
                                style={{
                                    padding: '10px 20px',
                                    backgroundColor: '#fff',
                                    color: '#000',
                                    fontSize: 14,
                                    fontWeight: 600,
                                    borderRadius: 8,
                                    transition: 'opacity 0.2s ease'
                                }}
                            >
                                Start Analysis
                            </Link>
                        </div>

                        {/* Mobile Menu Button */}
                        <button
                            onClick={() => setMobileOpen(!mobileOpen)}
                            className="mobile-menu-btn"
                            style={{
                                display: 'none',
                                padding: 8,
                                color: '#fff',
                                background: 'none',
                                border: 'none',
                                cursor: 'pointer'
                            }}
                        >
                            {mobileOpen ? <X style={{ width: 24, height: 24 }} /> : <Menu style={{ width: 24, height: 24 }} />}
                        </button>
                    </div>
                </div>
            </motion.nav>

            {/* Mobile Menu */}
            <AnimatePresence>
                {mobileOpen && (
                    <motion.div
                        initial={{ opacity: 0, y: -20 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -20 }}
                        style={{
                            position: 'fixed',
                            inset: 0,
                            zIndex: 40,
                            backgroundColor: '#000',
                            paddingTop: 80
                        }}
                    >
                        <div style={{ padding: '32px 24px' }}>
                            <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                                {navLinks.map((link, index) => (
                                    <motion.div
                                        key={link.href}
                                        initial={{ opacity: 0, x: -20 }}
                                        animate={{ opacity: 1, x: 0 }}
                                        transition={{ delay: index * 0.1 }}
                                    >
                                        <Link
                                            href={link.href}
                                            onClick={() => setMobileOpen(false)}
                                            style={{
                                                display: 'block',
                                                padding: '16px 0',
                                                fontSize: 24,
                                                fontWeight: 500,
                                                borderBottom: '1px solid rgba(255,255,255,0.1)',
                                                color: pathname === link.href ? '#fff' : 'rgba(255,255,255,0.6)'
                                            }}
                                        >
                                            {link.label}
                                        </Link>
                                    </motion.div>
                                ))}
                            </div>
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>

            {/* Responsive Styles */}
            <style jsx global>{`
        @media (max-width: 768px) {
          .desktop-nav, .desktop-cta {
            display: none !important;
          }
          .mobile-menu-btn {
            display: block !important;
          }
        }
      `}</style>
        </>
    );
}
