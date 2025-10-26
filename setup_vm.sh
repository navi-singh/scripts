#!/usr/bin/env bash
set -e

echo "🚀 Starting VM setup..."

# --- Install Oh My Zsh ---
if [ ! -d "$HOME/.oh-my-zsh" ]; then
  echo "Installing Oh My Zsh..."
  sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended
else
  echo "Oh My Zsh already installed."
fi

# --- Define ZSH_CUSTOM path ---
ZSH_CUSTOM=${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}

# --- Install Zsh Plugins ---
echo "Installing Zsh plugins..."

if [ ! -d "$ZSH_CUSTOM/plugins/zsh-autosuggestions" ]; then
  git clone https://github.com/zsh-users/zsh-autosuggestions "$ZSH_CUSTOM/plugins/zsh-autosuggestions"
else
  echo "zsh-autosuggestions already installed."
fi

if [ ! -d "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting" ]; then
  git clone https://github.com/zsh-users/zsh-syntax-highlighting.git "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting"
else
  echo "zsh-syntax-highlighting already installed."
fi

# --- Install Powerlevel10k Theme ---
if [ ! -d "$ZSH_CUSTOM/themes/powerlevel10k" ]; then
  git clone --depth=1 https://github.com/romkatv/powerlevel10k.git "$ZSH_CUSTOM/themes/powerlevel10k"
else
  echo "Powerlevel10k already installed."
fi

# --- Update .zshrc ---
if ! grep -q "zsh-autosuggestions" ~/.zshrc; then
  echo "Updating .zshrc plugins list..."
  sed -i.bak 's/plugins=(git)/plugins=(git zsh-autosuggestions zsh-syntax-highlighting)/' ~/.zshrc
  sed -i.bak 's|ZSH_THEME=.*|ZSH_THEME="powerlevel10k/powerlevel10k"|' ~/.zshrc
else
  echo ".zshrc already configured."
fi

# --- Install Tig from Source ---
echo "Installing Tig..."
cd /tmp
if [ ! -d "tig" ]; then
  git clone https://github.com/jonas/tig.git
fi
cd tig
make prefix=/usr/local
sudo make install prefix=/usr/local

echo "✅ Setup complete! You can now restart your terminal and enjoy Zsh + Powerlevel10k + Tig."
