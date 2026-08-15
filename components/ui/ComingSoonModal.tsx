"use client";

import React, { useState, useEffect } from "react";
import { X, Sparkles, CheckCircle2, AlertCircle, Loader2 } from "lucide-react";
import { subscribeUser } from "@/lib/api";

interface ComingSoonModalProps {
  isOpen?: boolean;
  onClose?: () => void;
}

export default function ComingSoonModal({ isOpen: controlledIsOpen, onClose }: ComingSoonModalProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [name, setName] = useState("");
  const [whatsapp, setWhatsapp] = useState("");
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");

  useEffect(() => {
    if (controlledIsOpen !== undefined) {
      setIsOpen(controlledIsOpen);
      return;
    }

    const dismissed = sessionStorage.getItem("bar_in_cairo_coming_soon_dismissed");
    if (!dismissed) {
      setIsOpen(true);
    }
  }, [controlledIsOpen]);

  const handleClose = () => {
    setIsOpen(false);
    sessionStorage.setItem("bar_in_cairo_coming_soon_dismissed", "true");
    if (onClose) onClose();
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg("");

    const cleanWa = whatsapp.trim();
    const cleanEmail = email.trim();
    const cleanName = name.trim();

    if (!cleanWa && !cleanEmail) {
      setErrorMsg("Please provide at least a WhatsApp number or Email so we can notify you.");
      return;
    }

    if (cleanWa && cleanWa.length < 8) {
      setErrorMsg("Please enter a valid WhatsApp number (at least 8 digits).");
      return;
    }

    if (cleanEmail && (!cleanEmail.includes("@") || !cleanEmail.includes("."))) {
      setErrorMsg("Please enter a valid email address.");
      return;
    }

    setLoading(true);
    try {
      const ok = await subscribeUser({
        name: cleanName || undefined,
        whatsapp_number: cleanWa || undefined,
        email: cleanEmail || undefined,
        source: "coming_soon_modal",
      });

      if (ok) {
        setSubmitted(true);
        setTimeout(() => {
          handleClose();
        }, 2200);
      } else {
        setErrorMsg("Failed to subscribe. Please try again in a moment.");
      }
    } catch {
      setErrorMsg("Something went wrong. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-xs animate-in fade-in duration-300">
      <div className="relative w-full max-w-lg overflow-hidden bg-[#24332d] text-[#ede7d8] border border-[#ad793b]/40 shadow-2xl p-6 sm:p-8 rounded-none font-sans">
        {/* Decorative corner accent */}
        <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-[#ad793b]/20 to-transparent pointer-events-none" />

        {/* Close Button */}
        <button
          onClick={handleClose}
          type="button"
          className="absolute top-4 right-4 p-2 text-[#c7bca4] hover:text-[#ede7d8] hover:bg-[#ad793b]/20 transition-colors duration-200 rounded-none focus:outline-none"
          aria-label="Close modal"
        >
          <X className="w-5 h-5" />
        </button>

        {submitted ? (
          <div className="py-8 text-center space-y-4 animate-in zoom-in-95 duration-300">
            <div className="inline-flex items-center justify-center w-14 h-14 rounded-full bg-[#ad793b]/20 text-[#ad793b]">
              <CheckCircle2 className="w-8 h-8" />
            </div>
            <h3 className="font-serif text-2xl sm:text-3xl text-[#ede7d8] font-bold tracking-tight">
              You&apos;re on the list!
            </h3>
            <p className="text-[#c7bca4] text-sm max-w-xs mx-auto">
              Thanks for dropping a line. We&apos;ll reach out as soon as everything is ready.
            </p>
          </div>
        ) : (
          <div className="space-y-6">
            {/* Header / Badge */}
            <div className="space-y-2">
              <div className="inline-flex items-center gap-1.5 px-2.5 py-1 text-xs font-mono tracking-wider uppercase bg-[#ad793b]/15 text-[#ad793b] border border-[#ad793b]/30">
                <Sparkles className="w-3.5 h-3.5" />
                <span>Under Construction</span>
              </div>

              <h2 className="font-serif text-2xl sm:text-3xl font-bold text-[#ede7d8] tracking-tight leading-tight">
                I&apos;m working on this now, it&apos;s coming soon.
              </h2>
              <p className="text-[#c7bca4] text-sm leading-relaxed">
                If you want to get notified when it&apos;s up, drop me a line below!
              </p>
            </div>

            {/* Form */}
            <form onSubmit={handleSubmit} className="space-y-4">
              {errorMsg && (
                <div className="flex items-start gap-2 p-3 text-xs bg-red-900/30 border border-red-500/40 text-red-200">
                  <AlertCircle className="w-4 h-4 text-red-400 shrink-0 mt-0.5" />
                  <span>{errorMsg}</span>
                </div>
              )}

              <div className="space-y-3">
                <div>
                  <label htmlFor="modal-name" className="block text-xs font-mono text-[#c7bca4] uppercase tracking-wider mb-1">
                    Name <span className="text-xs text-[#ad793b] font-sans lowercase">(optional)</span>
                  </label>
                  <input
                    id="modal-name"
                    type="text"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    placeholder="Your name"
                    className="w-full px-3 py-2 bg-[#1b2622] border border-[#ad793b]/30 text-[#ede7d8] placeholder-[#657067] text-sm focus:outline-none focus:border-[#ad793b] transition-colors"
                  />
                </div>

                <div>
                  <label htmlFor="modal-whatsapp" className="block text-xs font-mono text-[#c7bca4] uppercase tracking-wider mb-1">
                    WhatsApp <span className="text-xs text-[#ad793b] font-sans lowercase">(optional)</span>
                  </label>
                  <input
                    id="modal-whatsapp"
                    type="tel"
                    value={whatsapp}
                    onChange={(e) => setWhatsapp(e.target.value)}
                    placeholder="+201000000000"
                    className="w-full px-3 py-2 bg-[#1b2622] border border-[#ad793b]/30 text-[#ede7d8] placeholder-[#657067] text-sm focus:outline-none focus:border-[#ad793b] transition-colors"
                  />
                </div>

                <div>
                  <label htmlFor="modal-email" className="block text-xs font-mono text-[#c7bca4] uppercase tracking-wider mb-1">
                    Email <span className="text-xs text-[#ad793b] font-sans lowercase">(optional)</span>
                  </label>
                  <input
                    id="modal-email"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="you@example.com"
                    className="w-full px-3 py-2 bg-[#1b2622] border border-[#ad793b]/30 text-[#ede7d8] placeholder-[#657067] text-sm focus:outline-none focus:border-[#ad793b] transition-colors"
                  />
                </div>
              </div>

              <div className="pt-2 flex flex-col sm:flex-row items-center justify-between gap-3">
                <button
                  type="submit"
                  disabled={loading}
                  className="w-full sm:w-auto px-6 py-2.5 bg-[#ad793b] text-[#24332d] font-bold text-sm hover:bg-[#c78b43] focus:outline-none transition-colors flex items-center justify-center gap-2 cursor-pointer disabled:opacity-50"
                >
                  {loading ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span>Submitting...</span>
                    </>
                  ) : (
                    <span>Notify Me</span>
                  )}
                </button>

                <button
                  type="button"
                  onClick={handleClose}
                  className="text-xs font-mono text-[#c7bca4] hover:text-[#ede7d8] underline underline-offset-4 transition-colors"
                >
                  Explore site anyway &rarr;
                </button>
              </div>
            </form>
          </div>
        )}
      </div>
    </div>
  );
}
