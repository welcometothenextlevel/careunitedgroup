/* Care United Group — site behaviour. Vanilla JS, no libraries. */
(function () {
  "use strict";

  /* ---------- Footer year ---------- */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ---------- Sticky header shadow ---------- */
  var header = document.querySelector(".site-header");
  function onScroll() {
    if (header) header.classList.toggle("is-scrolled", window.scrollY > 8);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Mobile navigation ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (toggle && nav) {
    var closeNav = function (returnFocus) {
      toggle.setAttribute("aria-expanded", "false");
      toggle.setAttribute("aria-label", "Open menu");
      nav.classList.remove("is-open");
      if (returnFocus) toggle.focus();
    };
    toggle.addEventListener("click", function () {
      var open = toggle.getAttribute("aria-expanded") === "true";
      if (open) { closeNav(false); return; }
      toggle.setAttribute("aria-expanded", "true");
      toggle.setAttribute("aria-label", "Close menu");
      nav.classList.add("is-open");
      var first = nav.querySelector("a");
      if (first) first.focus();
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) closeNav(true);
    });
    document.addEventListener("click", function (e) {
      if (nav.classList.contains("is-open") && !nav.contains(e.target) && !toggle.contains(e.target)) closeNav(false);
    });
    nav.addEventListener("click", function (e) {
      if (e.target.closest("a") && nav.classList.contains("is-open")) closeNav(false);
    });
    /* Keep Tab inside the open menu on small screens */
    nav.addEventListener("keydown", function (e) {
      if (e.key !== "Tab" || !nav.classList.contains("is-open")) return;
      var items = [toggle].concat(Array.prototype.slice.call(nav.querySelectorAll("a")));
      var i = items.indexOf(document.activeElement);
      if (e.shiftKey && i === 1) { e.preventDefault(); toggle.focus(); }
      if (!e.shiftKey && i === items.length - 1) { e.preventDefault(); toggle.focus(); }
    });
    window.matchMedia("(min-width: 1000px)").addEventListener("change", function (mq) {
      if (mq.matches) closeNav(false);
    });
  }

  /* ---------- Gentle reveal on scroll ----------
     Content is visible without JS; the "js" class on <html> sets the start state.
     Opacity/transform only (no clip-path), and a failsafe shows everything. */
  var reveals = document.querySelectorAll(".reveal, .veil");
  var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  function showAll() { reveals.forEach(function (el) { el.classList.add("is-in"); }); }
  if (!("IntersectionObserver" in window) || reduce) {
    showAll();
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) { entry.target.classList.add("is-in"); io.unobserve(entry.target); }
      });
    }, { rootMargin: "0px", threshold: 0 });
    reveals.forEach(function (el) { io.observe(el); });
    /* Hidden tabs and print never fire the observer: show everything */
    setTimeout(function () { if (document.visibilityState === "hidden") showAll(); }, 1500);
    window.addEventListener("beforeprint", showAll);
  }

  /* ---------- Services showcase: tabs on wide screens, stacked cards on small ones ---------- */
  document.querySelectorAll("[data-tabs]").forEach(function (root) {
    var tabs = Array.prototype.slice.call(root.querySelectorAll("[data-tab]"));
    var panels = Array.prototype.slice.call(root.querySelectorAll("[data-panel]"));
    var list = root.querySelector(".svc-tablist");
    var wide = window.matchMedia("(min-width: 900px)");
    var current = 0;

    function select(i, focus) {
      current = i;
      tabs.forEach(function (t, n) {
        var on = n === i;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        panels[n].classList.toggle("is-active", on);
      });
      if (focus) tabs[i].focus();
    }
    function setMode() {
      if (wide.matches) {
        list.setAttribute("role", "tablist");
        tabs.forEach(function (t, n) {
          t.setAttribute("role", "tab");
          t.setAttribute("aria-controls", panels[n].id);
          panels[n].setAttribute("role", "tabpanel");
          panels[n].setAttribute("aria-labelledby", t.id);
          panels[n].tabIndex = 0;
        });
        select(current, false);
      } else {
        list.removeAttribute("role");
        tabs.forEach(function (t, n) {
          ["role", "aria-controls", "aria-selected"].forEach(function (a) { t.removeAttribute(a); });
          ["role", "aria-labelledby", "tabindex"].forEach(function (a) { panels[n].removeAttribute(a); });
        });
      }
    }
    tabs.forEach(function (t, n) {
      t.addEventListener("click", function () { select(n, false); });
      t.addEventListener("keydown", function (e) {
        var k = e.key, next = null;
        if (k === "ArrowDown" || k === "ArrowRight") next = (n + 1) % tabs.length;
        if (k === "ArrowUp" || k === "ArrowLeft") next = (n - 1 + tabs.length) % tabs.length;
        if (k === "Home") next = 0;
        if (k === "End") next = tabs.length - 1;
        if (next !== null) { e.preventDefault(); select(next, true); }
      });
    });
    wide.addEventListener("change", setMode);
    setMode();
  });

  /* ---------- Quote forms ---------- */
  var SERVICE_PARAM = { health: "Health assistance", home: "Home care", daily: "Support with daily personal activities", community: "Community participation", transport: "Transport in our wheelchair-accessible van" };

  document.querySelectorAll("form[data-quote-form]").forEach(function (form) {
    var summary = form.querySelector(".form-summary");
    var summaryList = summary ? summary.querySelector("ul") : null;
    var submitBtn = form.querySelector("[type=submit]");
    var card = form.closest(".form-card");
    var success = card ? card.querySelector(".form-success") : null;
    var sendError = form.querySelector(".form-error-send");

    /* Pre-tick a service from ?service=health etc. */
    var wanted = new URLSearchParams(window.location.search).get("service");
    if (wanted && SERVICE_PARAM[wanted]) {
      form.querySelectorAll('input[name="services"]').forEach(function (box) {
        if (box.value === SERVICE_PARAM[wanted]) box.checked = true;
      });
    }

    function setError(key, message) {
      var holder = form.querySelector('[data-field="' + key + '"]');
      if (!holder) return;
      var msg = holder.querySelector(".error-msg");
      var targets = key === "services" ? holder.querySelectorAll("input") : [holder.querySelector("input, select, textarea")];
      if (msg) msg.textContent = message || "";
      Array.prototype.forEach.call(targets, function (t) {
        if (!t) return;
        if (message) t.setAttribute("aria-invalid", "true");
        else t.removeAttribute("aria-invalid");
      });
    }

    function checks() {
      var errors = [];
      var name = form.elements.name.value.trim();
      var phone = form.elements.phone.value.trim();
      var email = form.elements.email ? form.elements.email.value.trim() : "";
      var services = form.querySelectorAll('input[name="services"]:checked').length;
      var consent = form.elements.consent;
      var digits = phone.replace(/[^\d]/g, "");

      if (!name) errors.push(["name", "Please tell us your name."]);
      else if (name.length < 2) errors.push(["name", "Please enter your full name."]);

      if (!phone) errors.push(["phone", "Please add a phone number so we can call you back."]);
      else if (digits.length < 8 || digits.length > 12) errors.push(["phone", "That phone number looks too short or too long. Please check it, for example 0412 345 678."]);

      if (email && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) errors.push(["email", "That email address doesn't look quite right. Please check it, or leave it blank."]);

      if (!services) errors.push(["services", "Please choose at least one service you're interested in."]);

      if (consent && !consent.checked) errors.push(["consent", "Please tick the box so we can contact you about your enquiry."]);
      return errors;
    }

    function clearAll() {
      ["name", "phone", "email", "services", "consent"].forEach(function (k) { setError(k, ""); });
      if (summary) summary.classList.remove("is-visible");
    }

    /* Re-check a field once the person has fixed it */
    form.addEventListener("change", function (e) {
      if (!form.dataset.tried) return;
      var errs = checks();
      var key = e.target.name === "services" ? "services" : e.target.name;
      var found = errs.filter(function (x) { return x[0] === key; })[0];
      setError(key, found ? found[1] : "");
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      form.dataset.tried = "1";
      clearAll();
      if (sendError) sendError.classList.remove("is-visible");

      var errors = checks();
      if (errors.length) {
        errors.forEach(function (x) { setError(x[0], x[1]); });
        if (summary && summaryList) {
          summaryList.innerHTML = "";
          errors.forEach(function (x) {
            var li = document.createElement("li");
            var a = document.createElement("a");
            var id = form.id + "-" + x[0];
            a.href = "#" + id;
            a.textContent = x[1];
            a.addEventListener("click", function (ev) {
              ev.preventDefault();
              var el = document.getElementById(id);
              if (el) el.focus();
            });
            li.appendChild(a);
            summaryList.appendChild(li);
          });
          summary.classList.add("is-visible");
          summary.focus();
        }
        return;
      }

      /* Honeypot: bots fill hidden fields. Pretend it worked. */
      if (form.elements._gotcha && form.elements._gotcha.value) { showSuccess(); return; }

      var action = form.getAttribute("action") || "";
      /* TODO: until the Formspree ID is replaced, the form runs in preview mode
         and shows the thank-you message without sending anything. */
      if (action.indexOf("YOUR_FORM_ID") !== -1) {
        if (window.console) console.info("Quote form is in preview mode: replace YOUR_FORM_ID with the real Formspree form ID.");
        showSuccess();
        return;
      }

      submitBtn.disabled = true;
      var label = submitBtn.querySelector("span");
      var original = label ? label.textContent : "";
      if (label) label.textContent = "Sending…";

      fetch(action, { method: "POST", body: new FormData(form), headers: { Accept: "application/json" } })
        .then(function (res) {
          if (!res.ok) throw new Error("Bad response " + res.status);
          showSuccess();
        })
        .catch(function () {
          if (sendError) { sendError.classList.add("is-visible"); sendError.focus(); }
        })
        .finally(function () {
          submitBtn.disabled = false;
          if (label) label.textContent = original;
        });
    });

    function showSuccess() {
      form.reset();
      if (!success) return;
      form.hidden = true;
      var intro = card.querySelector(".form-head");
      if (intro) intro.hidden = true;
      success.classList.add("is-visible");
      success.focus();
      var top = card.getBoundingClientRect().top + window.scrollY - 110;
      window.scrollTo({ top: top, behavior: reduce ? "auto" : "smooth" });
    }
  });
})();
