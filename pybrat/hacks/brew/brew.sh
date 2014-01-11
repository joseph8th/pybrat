
#[brew]
PYBREW_DEF_ROOTD=~/.pythonbrew
PYBREW_DEF_PYD=~/.pythonbrew/pythons
PYBREW_DEF_VENVD=~/.pythonbrew/venvs

#[mgrs]
AVAIL_MGRS="pymgr venvmgr"

# Function to configure shell configuration for pythonbrew if user wants
function _config_shrc_brew {

    echo; read -p "Configure 'pythonbrew' in your '~/.bashrc'? [y/N]: "
    if [[ "$REPLY" != "y" ]]; then
	printf "\n==> ERROR: 'pythonbrew' needs to be configured to work!\n"
	_err; return
    fi

    printf "\n# 'pythonbrew' environment configuration\n" >> ${HOME}/.bashrc
    echo "[[ -s ${HOME}/.pythonbrew/etc/bashrc ]] && source ${HOME}/.pythonbrew/etc/bashrc" \
	>> ${HOME}/.bashrc

    echo '==> DONE! You need to restart your shell. Type `exec $SHELL`.'
    printf "(On uninstall, delete 'pythonbrew' section from '${HOME}/.bashrc'.)\n\n"

    return
}



# Check if 'pythonbrew' installed and if not, install.
function _check_req_brew {

    _search_path "${PYBREW_DEF_ROOTD}/bin"
    [[ "$FIND_PATH" == "0" ]] && return

    if [ -e "$PYBREW_DEF_ROOTD" ]; then
	echo "==> ERROR: 'pythonbrew' installed but not configured."
	echo "Did you configure your shell script and type 'exec $SHELL'?"
        _config_shrc_brew
	_err; return
    fi

    # good to install ...
    echo "==> This version still requires (deprecated) 'pythonbrew'."
    read -p "Use 'curl' to install 'pythonbrew' to defaults? [y/N]: "
    [[ "$REPLY" != "y" ]] && _err && return

    # ... so curl it all to defaults
    echo
    curl -kL http://xrl.us/pythonbrewinstall | bash
    if [ ! -e "${PYBREW_DEF_ROOTD}" ]; then
	echo "==> ERROR: 'pythonbrew' did not install correctly."
	_err; return
    fi

    _config_shrc_brew
    return
}
