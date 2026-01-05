from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings

from accounts.models import Student
from home.models import DareExchange

import requests
import json
import re


# =========================
# DASHBOARD
# =========================
@login_required
def dashboard(request):
    student, _ = Student.objects.get_or_create(user=request.user)

    created_dares = DareExchange.objects.filter(
        user=request.user
    ).order_by("-id")

    accepted_dares = DareExchange.objects.filter(
        accepted_by=request.user
    ).order_by("-id")

    return render(request, "dashboard/index.html", {
        "student": student,
        "created_dares": created_dares,
        "accepted_dares": accepted_dares,
        "page": "dashboard",
    })


# =========================
# VIEW SINGLE DARE
# =========================
@login_required
def view_dare(request, id):
    dare = get_object_or_404(DareExchange, id=id, user=request.user)
    return render(request, "dashboard/view_dare.html", {"dare": dare})


# =========================
# DELETE DARE
# =========================
@login_required
def delete_dare(request, id):
    dare = get_object_or_404(DareExchange, id=id, user=request.user)
    dare.delete()
    return redirect("current_dares")


# =========================
# EDIT DARE
# =========================
@login_required
def edit_dare(request, id):
    dare = get_object_or_404(DareExchange, id=id, user=request.user)

    if request.method == "POST":
        dare.Name = request.POST.get("Name")
        dare.Email = request.POST.get("Email")
        dare.DareTitle = request.POST.get("DareTitle")
        dare.Description = request.POST.get("Description")
        dare.Difficulty = request.POST.get("Difficulty")
        dare.Category = request.POST.get("Category")
        dare.Deadline = request.POST.get("Deadline")
        dare.Tags = request.POST.get("Tags")
        dare.is_edited = True
        dare.save()
        return redirect("current_dares")

    return render(request, "home/edit_dare.html", {"dare": dare})


# =========================
# CREATE DARE
# =========================
@login_required
def create_dare(request):
    if request.method == "POST":
        DareExchange.objects.create(
            user=request.user,
            Name=request.POST.get("Name"),
            Email=request.POST.get("Email"),
            DareTitle=request.POST.get("DareTitle"),
            Description=request.POST.get("Description"),
            Difficulty=request.POST.get("Difficulty"),
            Category=request.POST.get("Category"),
            Deadline=request.POST.get("Deadline"),
            Tags=request.POST.get("Tags"),
        )
        return redirect("current_dares")

    # Prefill from AI
    initial_data = {
        "title": request.GET.get("title", ""),
        "description": request.GET.get("description", ""),
        "difficulty": request.GET.get("difficulty", ""),
    }

    return render(request, "home/create_dare.html", {
        "initial_data": initial_data
    })


# =========================
# AI DARE GENERATOR (GROQ)
# =========================
@login_required
def ask_ai(request):
    context = {
        "response": None,
        "user_prompt": "",
        "error": None,
    }

    if request.method == "POST":
        user_prompt = request.POST.get("prompt", "").strip()
    else:
        user_prompt = request.GET.get("prompt", "").strip()

    context["user_prompt"] = user_prompt

    if user_prompt:
        dares = generate_response(user_prompt)
        if dares:
            context["response"] = dares
        else:
            context["error"] = "Failed to generate dares. Please try again."

    return render(request, "dashboard/ask_ai.html", context)


# =========================
# GROQ API LOGIC
# =========================

def generate_response(query):
    try:
        import requests, json, re
        from django.conf import settings

        print("🔵 generate_response CALLED")
        print("🔵 QUERY:", query)

        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {settings.GROQ_API_KEY}",
            "Content-Type": "application/json",
        }

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a JSON generator. "
                        "You must return VALID JSON ONLY. "
                        "Do not explain anything."
                    ),
                },
                {
                    "role": "user",
                    "content": (
                        "Generate EXACTLY 5 fun and safe dares.\n"
                        "Return ONLY a JSON array.\n"
                        "Each object must contain:\n"
                        "- title (string)\n"
                        "- description (string)\n"
                        "- difficulty (Easy, Medium, Hard)\n\n"
                        f"User request: {query}"
                    ),
                },
            ],
            "temperature": 0.7,
        }

        response = requests.post(url, headers=headers, json=payload, timeout=30)

        print("🟡 STATUS CODE:", response.status_code)
        print("🟡 RAW RESPONSE:", response.text)

        if response.status_code != 200:
            return None

        data = response.json()
        raw_text = data["choices"][0]["message"]["content"].strip()

        print("🟢 MODEL OUTPUT:", raw_text)

        # ✅ TRY NORMAL JSON FIRST
        try:
            return json.loads(raw_text)
        except json.JSONDecodeError:
            pass

        # ✅ FALLBACK: EXTRACT JSON ARRAY
        match = re.search(r"\[\s*\{.*\}\s*\]", raw_text, re.DOTALL)
        if not match:
            print("❌ NO JSON ARRAY FOUND")
            return None

        cleaned = match.group()

        # Fix common quote issues
        cleaned = cleaned.replace('“', '"').replace('”', '"')

        try:
            return json.loads(cleaned)
        except Exception as e:
            print("🔥 FINAL JSON ERROR:", e)
            return None

    except Exception as e:
        print("🔥 EXCEPTION:", e)
        return None




