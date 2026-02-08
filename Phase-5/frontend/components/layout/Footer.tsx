/**
 * Footer - Beautiful footer with links and branding
 */
"use client"

import { motion } from "framer-motion"
import { CheckSquare, Github, Twitter, Linkedin, Mail, Heart } from "lucide-react"
import Link from "next/link"

interface FooterProps {
  variant?: "light" | "dark"
}

export function Footer({ variant = "dark" }: FooterProps) {
  const isDark = variant === "dark"

  const links = {
    product: [
      { label: "Features", href: "#features" },
      { label: "Pricing", href: "#pricing" },
      { label: "Demo", href: "/dashboard" },
      { label: "Updates", href: "#updates" },
    ],
    company: [
      { label: "About", href: "#about" },
      { label: "Blog", href: "#blog" },
      { label: "Careers", href: "#careers" },
      { label: "Contact", href: "#contact" },
    ],
    resources: [
      { label: "Documentation", href: "#docs" },
      { label: "Help Center", href: "#help" },
      { label: "Community", href: "#community" },
      { label: "Status", href: "#status" },
    ],
    legal: [
      { label: "Privacy", href: "#privacy" },
      { label: "Terms", href: "#terms" },
      { label: "Security", href: "#security" },
      { label: "Cookies", href: "#cookies" },
    ],
  }

  const socials = [
    { icon: Github, href: "https://github.com/MSohaibShahzad", label: "GitHub" },
    { icon: Twitter, href: "https://twitter.com", label: "Twitter" },
    { icon: Linkedin, href: "https://linkedin.com", label: "LinkedIn" },
    { icon: Mail, href: "mailto:hello@nexustasks.com", label: "Email" },
  ]

  return (
    <footer className={isDark ? "bg-[#0F172A] text-white" : "bg-gray-50 text-gray-900"}>
      <div className="container mx-auto px-6 py-12">
        {/* Main Footer Content */}
        <div className="grid grid-cols-2 md:grid-cols-6 gap-8 mb-8">
          {/* Brand Section */}
          <div className="col-span-2">
            <Link href="/" className="flex items-center gap-2 mb-4 group">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-[#06B6D4] to-[#10B981] flex items-center justify-center group-hover:scale-110 transition-transform">
                <CheckSquare className="w-6 h-6 text-white" />
              </div>
              <div className="flex flex-col">
                <span className="text-xl font-bold">Nexus</span>
                <span className="text-xs -mt-1 opacity-80">tasks</span>
              </div>
            </Link>
            <p className={`text-sm mb-4 max-w-xs ${isDark ? "text-white/70" : "text-gray-600"}`}>
              Manage your tasks beautifully. Stay organized, focused, and productive with Nexus tasks.
            </p>
            {/* Social Links */}
            <div className="flex gap-3">
              {socials.map((social) => (
                <motion.a
                  key={social.label}
                  href={social.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={`w-9 h-9 rounded-lg flex items-center justify-center transition-colors ${
                    isDark
                      ? "bg-white/10 hover:bg-white/20"
                      : "bg-gray-200 hover:bg-gray-300"
                  }`}
                  whileHover={{ scale: 1.1, y: -2 }}
                  whileTap={{ scale: 0.95 }}
                  aria-label={social.label}
                >
                  <social.icon className="w-4 h-4" />
                </motion.a>
              ))}
            </div>
          </div>

          {/* Product Links */}
          <div>
            <h3 className="font-semibold mb-4 text-sm uppercase tracking-wider">Product</h3>
            <ul className="space-y-2">
              {links.product.map((link) => (
                <li key={link.label}>
                  <Link
                    href={link.href}
                    className={`text-sm transition-colors ${
                      isDark
                        ? "text-white/70 hover:text-white"
                        : "text-gray-600 hover:text-[#3B82F6]"
                    }`}
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Company Links */}
          <div>
            <h3 className="font-semibold mb-4 text-sm uppercase tracking-wider">Company</h3>
            <ul className="space-y-2">
              {links.company.map((link) => (
                <li key={link.label}>
                  <Link
                    href={link.href}
                    className={`text-sm transition-colors ${
                      isDark
                        ? "text-white/70 hover:text-white"
                        : "text-gray-600 hover:text-[#3B82F6]"
                    }`}
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Resources Links */}
          <div>
            <h3 className="font-semibold mb-4 text-sm uppercase tracking-wider">Resources</h3>
            <ul className="space-y-2">
              {links.resources.map((link) => (
                <li key={link.label}>
                  <Link
                    href={link.href}
                    className={`text-sm transition-colors ${
                      isDark
                        ? "text-white/70 hover:text-white"
                        : "text-gray-600 hover:text-[#3B82F6]"
                    }`}
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Legal Links */}
          <div>
            <h3 className="font-semibold mb-4 text-sm uppercase tracking-wider">Legal</h3>
            <ul className="space-y-2">
              {links.legal.map((link) => (
                <li key={link.label}>
                  <Link
                    href={link.href}
                    className={`text-sm transition-colors ${
                      isDark
                        ? "text-white/70 hover:text-white"
                        : "text-gray-600 hover:text-[#3B82F6]"
                    }`}
                  >
                    {link.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className={`pt-8 border-t ${isDark ? "border-white/10" : "border-gray-200"}`}>
          <div className="flex flex-col md:flex-row justify-between items-center gap-4">
            <p className={`text-sm ${isDark ? "text-white/60" : "text-gray-600"}`}>
              © {new Date().getFullYear()} Nexus tasks. All rights reserved.
            </p>
            <p className={`text-sm flex items-center gap-1 ${isDark ? "text-white/60" : "text-gray-600"}`}>
              Made with <Heart className="w-4 h-4 text-red-500 fill-current" /> by{" "}
              <a
                href="https://github.com/MSohaibShahzad"
                target="_blank"
                rel="noopener noreferrer"
                className={`font-medium transition-colors ${
                  isDark
                    ? "text-[#06B6D4] hover:text-[#10B981]"
                    : "text-[#3B82F6] hover:text-[#06B6D4]"
                }`}
              >
                Sohaib Shahzad
              </a>
            </p>
          </div>
        </div>
      </div>
    </footer>
  )
}
