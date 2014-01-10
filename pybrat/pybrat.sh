#[pybrat]
REQ_PYVER='2.7'
PYBRAT_DEF_INSTALL=/home/${USER}/.pybrat
PYBRAT_DEF_COMMANDD=/usr/local
PYBRAT_DEF_ROOTD=/home/${USER}/.pybrat
PYBRAT_DEF_PROJD=/home/${USER}/.config/pybrat
PYBRAT_DEF_MAINF=${PYBRAT_DEF_ROOTD}/pybrat.py


# configure the shell script for pybrat
function _config_shrc_pybrat {

    echo; read -p "Configure 'pybrat' in your '~/.bashrc'? [y/N]: "
    if [[ "$REPLY" != "y" ]]; then
	printf "\n==> 'pybrat' needs to be configured to work!\n"
	_err; return
    fi

    printf "\n# 'pybrat' environment configuration\n" >> ${HOME}/.bashrc
    echo "[[ -s ${HOME}/.pybrat/data/bashrc ]] && source ${HOME}/.pybrat/data/bashrc" \
	>> ${HOME}/.bashrc

    echo; echo '==> DONE! You need to restart your shell. Type `exec $SHELL`.'
    printf "(On uninstall, delete 'pybrat' section from '${HOME}/.bashrc'.)\n\n"

    return
}

