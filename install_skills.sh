#!/bin/bash
# 批量安装OpenClaw技能脚本

SKILLS=(
  "coding-agent"
  "discord"
  "slack"
  "notion"
  "obsidian"
  "himalaya"
  "mcporter"
  "clawhub"
  "healthcheck"
  "skill-creator"
)

echo "开始批量安装技能..."
for skill in "${SKILLS[@]}"; do
  echo "Installing: $skill"
  npx clawhub install "$skill" --force 2>&1 | grep -E "(OK|Error|installed)" || true
  sleep 5  # 避免限速
done

echo "安装完成"
