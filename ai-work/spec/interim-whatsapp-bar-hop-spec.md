# Architectural Specification: Interim Personal Bar Crawl WhatsApp Box

**Document Path**: `ai-work/spec/interim-whatsapp-bar-hop-spec.md`  
**Feature Goal**: Replace the current subscription input box with a personal, warm, and friendly direct contact CTA connecting visitors to a custom Downtown Cairo Bar Crawl via WhatsApp (`wa.me`) and Email (`mailto:`).  
**Author**: `cairo-architect`  
**Date**: 2026-08-13  
**Status**: Approved Specification  

---

## 1. Objective

Provide an engaging, conversion-focused interim contact section on `barincairo.com`. Instead of a generic input box, this section welcomes visitors with a personal, friendly tone, inviting them to connect directly with the founder on WhatsApp for a customized, fun Downtown Cairo bar crawl and nightlife heritage walk.

---

## 2. Scope & Boundaries

### 2.1 In-Scope Target Modules
- `app/page.tsx`
- `components/ui/PersonalCrawlCard.tsx` (or updated `#subscribe` hero/footer component)
- `lib/config.ts` (WhatsApp phone number & contact email configuration constants)
- `__tests__/PersonalCrawlCard.test.tsx`

### 2.2 Out-of-Scope / Non-Goals
- Automated WhatsApp Cloud API webhooks or phone verification services (deferred to future automated dispatch phase).
- Backend database schema changes to `subscribers` table.

---

## 3. Architecture & UI Component Specifications

### 3.1 Content & Copy Strategy
- **Tone**: Warm, friendly, welcoming, personal. Zero technical jargon or references to "automation" / "building in progress".
- **Headline**: *"Want a Personal Downtown Cairo Bar Hop?"*
- **Body Copy**: *"Hey there! We love Downtown Cairo's historic bars, hidden passage bistros, and rooftop breezes. Looking for a friendly, customized night out? Message Alex directly on WhatsApp and let's craft a fun bar crawl tailored to your vibe!"*
- **Primary CTA Button**: *"Chat on WhatsApp"* (`https://wa.me/2010...` with pre-filled message: `"Hey Alex! I'm on barincairo.com and would love to organize a custom bar crawl!"`)
- **Secondary CTA Link**: *"Or send an email"* (`mailto:alex.seif@gmail.com?subject=Custom%20Cairo%20Bar%20Hop`)

### 3.2 TypeScript Component Interface (`components/ui/PersonalCrawlCard.tsx`)
```typescript
export interface PersonalCrawlCardProps {
  whatsappNumber: string
  contactEmail: string
  className?: string
}
```

### 3.3 Configuration Constants (`lib/config.ts`)
```typescript
export const CONTACT_CONFIG = {
  WHATSAPP_NUMBER: process.env.NEXT_PUBLIC_WHATSAPP_NUMBER || '201000000000',
  CONTACT_EMAIL: process.env.NEXT_PUBLIC_CONTACT_EMAIL || 'alex.seif@gmail.com',
  DEFAULT_WA_MESSAGE: 'Hey Alex! I am on barincairo.com and would love to organize a custom bar crawl!',
}
```

---

## 4. Khedivial Aesthetic & UI Tokens

- **Card Container**: `border-2 border-[#24332d] bg-[#ede7d8] p-6 shadow-[4px_4px_0px_#24332d]`
- **Primary WhatsApp Button**:
  - Background: `#24332d` (Deep Khedivial Olive)
  - Text: `#ede7d8` (Limestone Parchment)
  - Hover: `hover:bg-[#ad793b]` (Egyptian Gold Accent)
  - Minimum Touch Target: **44px $\times$ 44px** (`h-12 px-6 flex items-center justify-center`)
- **Secondary Email Button / Link**:
  - Border: `border border-[#24332d]`
  - Text: `#24332d`
  - Minimum Touch Target: **44px height**

---

## 5. Security & Safety Compliance (SEC-1.1 to SEC-1.5)

- [ ] **SEC-1.1**: External WhatsApp and mailto links properly encoded via `encodeURIComponent` to prevent XSS or broken URL structures.
- [ ] **SEC-1.4**: Phone numbers and email defaults configured via environment constants with fallback defaults (`NEXT_PUBLIC_WHATSAPP_NUMBER`).
- [ ] **SEC-1.5**: All external link tags (`<a>`) set strictly with `target="_blank"` and `rel="noopener noreferrer"`.
- [ ] **Khedivial Matrix**: Minimum 44px touch target thresholds and hex palette (`#ede7d8`, `#24332d`, `#ad793b`) strictly met.

---

## 6. Testing Strategy

- **Vitest**: Create `__tests__/PersonalCrawlCard.test.tsx` verifying:
  - Correct rendering of friendly headline and body copy.
  - Proper formatting of `wa.me` URL with encoded pre-filled text message.
  - Proper formatting of `mailto:` link.
  - Verification that 44px minimum touch targets and accessibility attributes (`aria-label`) exist on buttons.

---

## 7. Handoff Instructions

1. **Create Configuration**: Add `CONTACT_CONFIG` in `lib/config.ts` loading environment variables.
2. **Build Component**: Create `components/ui/PersonalCrawlCard.tsx` following the Khedivial design matrix.
3. **Update Home Page**: Integrate the personal crawl card into `app/page.tsx` replacing the current subscriber form.
4. **Add Unit Test**: Create `__tests__/PersonalCrawlCard.test.tsx`.
5. **Verification**: Run `npm test -- --run` ensuring 100% test pass rate with 0 TypeScript/lint warnings.
