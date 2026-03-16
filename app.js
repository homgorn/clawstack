(function () {
  const metaApiBase = document.querySelector('meta[name="clawstack-api-base"]');
  const fallbackApiBase = (metaApiBase && metaApiBase.content.trim()) || "/api";
  const form = document.querySelector("[data-intake-form]");
  const statusNode = document.querySelector("[data-form-status]");
  const tierLinks = document.querySelectorAll("[data-service-tier]");
  const repoLinks = document.querySelectorAll('[data-site-link="repo"]');
  const docLinks = document.querySelectorAll("[data-doc-label]");
  const contactLink = document.querySelector("[data-contact-email]");
  const apiBaseNode = document.querySelector("[data-public-api-base]");
  const offerNodes = document.querySelectorAll("[data-offer]");

  let apiBase = fallbackApiBase.replace(/\/$/, "");
  let contactEmail = null;
  let siteConfigPromise = null;

  function applySiteConfig(payload) {
    if (!payload || typeof payload !== "object") {
      return;
    }
    if (typeof payload.public_api_base === "string" && payload.public_api_base) {
      apiBase = payload.public_api_base.replace(/\/$/, "");
    } else if (typeof payload.public_api_url === "string" && payload.public_api_url) {
      apiBase = payload.public_api_url.replace(/\/$/, "");
    }
    if (apiBaseNode) {
      apiBaseNode.textContent = apiBase;
    }
    if (typeof payload.repo_url === "string" && payload.repo_url) {
      for (const link of repoLinks) {
        link.href = payload.repo_url;
      }
    }
    if (typeof payload.contact_email === "string" && payload.contact_email) {
      contactEmail = payload.contact_email;
      if (contactLink) {
        contactLink.href = `mailto:${contactEmail}`;
        contactLink.textContent = contactEmail;
      }
    }
    if (Array.isArray(payload.docs) && payload.docs.length) {
      const docMap = new Map();
      for (const doc of payload.docs) {
        if (doc && typeof doc.label === "string" && typeof doc.href === "string") {
          docMap.set(doc.label, doc.href);
        }
      }
      if (docMap.size) {
        for (const link of docLinks) {
          const label = link.getAttribute("data-doc-label");
          if (label && docMap.has(label)) {
            link.href = docMap.get(label);
          }
        }
      }
    }

    if (Array.isArray(payload.offers) && payload.offers.length && offerNodes.length) {
      for (const offer of payload.offers) {
        if (!offer || typeof offer.slug !== "string") {
          continue;
        }
        const card = document.querySelector(`[data-offer="${offer.slug}"]`);
        if (!card) {
          continue;
        }
        const titleNode = card.querySelector("[data-offer-title]");
        const priceNode = card.querySelector("[data-offer-price]");
        const summaryNode = card.querySelector("[data-offer-summary]");
        const ctaNode = card.querySelector("[data-offer-cta]");

        if (titleNode && typeof offer.title === "string") {
          titleNode.textContent = offer.title;
        }
        if (priceNode && typeof offer.price_label === "string") {
          priceNode.textContent = offer.price_label;
        }
        if (summaryNode && typeof offer.summary === "string") {
          summaryNode.textContent = offer.summary;
        }
        if (ctaNode) {
          if (typeof offer.cta_label === "string") {
            ctaNode.textContent = offer.cta_label;
          }
          if (typeof offer.cta_href === "string") {
            ctaNode.href = offer.cta_href;
          }
        }
      }
    }
  }

  async function loadSiteConfig() {
    if (!siteConfigPromise) {
      siteConfigPromise = (async () => {
        const candidates = [
          `${apiBase}/v1/site-config`,
          "/v1/site-config",
          "/site-config.json"
        ];
        for (const url of candidates) {
          try {
            const response = await fetch(url, {
              method: "GET",
              headers: { Accept: "application/json" }
            });
            if (!response.ok) {
              continue;
            }
            return await response.json();
          } catch (_error) {
            continue;
          }
        }
        return null;
      })();
    }

    const payload = await siteConfigPromise;
    if (!payload) {
      siteConfigPromise = null;
      return null;
    }
    applySiteConfig(payload);
    return payload;
  }

  function setStatus(message, isError) {
    if (!statusNode) {
      return;
    }
    statusNode.textContent = message;
    statusNode.dataset.state = isError ? "error" : "success";
  }

  if (form) {
    for (const link of tierLinks) {
      link.addEventListener("click", function () {
        const tier = link.getAttribute("data-service-tier");
        const select = form.querySelector('select[name="service_tier"]');
        if (tier && select) {
          select.value = tier;
        }
      });
    }
  }

  if (form) {
    form.addEventListener("submit", async function (event) {
      event.preventDefault();
      setStatus("Sending request...", false);

      const data = new FormData(form);
      const payload = {
        service_tier: String(data.get("service_tier") || ""),
        name: String(data.get("name") || "").trim(),
        email: String(data.get("email") || "").trim(),
        company: String(data.get("company") || "").trim() || null,
        source: window.location.href,
        website: String(data.get("website") || "").trim() || null,
        message: String(data.get("message") || "").trim()
      };

      try {
        await loadSiteConfig();
        const response = await fetch(`${apiBase}/v1/intake`, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json"
          },
          body: JSON.stringify(payload)
        });

        if (!response.ok) {
          const body = await response.text();
          throw new Error(body || `Request failed with status ${response.status}`);
        }

        form.reset();
        setStatus("Request accepted. You can now wire this into email, CRM, or support flows.", false);
      } catch (_error) {
        const fallback = contactEmail
          ? `Could not reach the intake API. You can also email ${contactEmail}.`
          : "Could not reach the intake API. Check backend URL or reverse proxy routing.";
        setStatus(fallback, true);
      }
    });
  }

  void loadSiteConfig();
})();
