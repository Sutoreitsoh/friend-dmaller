import base64 as b64, requests as rq, os as _o, time as _t, logging as lg
from PyQt5.QtWidgets import QMainWindow as QMW, QWidget as QW, QHBoxLayout as QHB, QVBoxLayout as QVB
from PyQt5.QtWidgets import QPushButton as QB, QLabel as QL, QTextEdit as QE, QStackedWidget as QSW, QApplication as QApp
from PyQt5.QtCore import Qt as _Qt
from .sidebar import A as Sb
from .settings import Settings as St
from logic.token_manager import TokenManager as TM
import os
import sys
class Z(QMW):
    def get_asset_path(filename):
        if hasattr(sys, '_MEIPASS'):
            base = sys._MEIPASS
        else:
            base = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets"))
        return os.path.join(base, filename)
    def __init__(self):
        self._ensure_files()
        super().__init__()
        self.setWindowTitle("Straizo's Dmall App")
        self.setGeometry(100, 100, 1000, 700)
        style_path = Z.get_asset_path("styles.qss")
        with open(style_path, "r", encoding="utf-8") as f:
            self.setStyleSheet(f.read())
        _w = QW()
        _l = QHB(_w)

        self._s = Sb(self)
        _l.addWidget(self._s, 0)

        self._stk = QSW()
        self._db = QW()
        _db_l = QVB(self._db)

        self._btn = QB("Friend Dmall")
        self._btn.clicked.connect(self._a)
        _db_l.addWidget(self._btn)

        self._log = QE()
        self._log.setReadOnly(True)
        _db_l.addWidget(QL("Logs:"))
        _db_l.addWidget(self._log)

        self._stk.addWidget(self._db)
        _l.addWidget(self._stk, 1)
        self.setCentralWidget(_w)

    def _ensure_files(self):
        base_dir = os.getcwd()
        files_defaults = {
            "tokens.txt": "",
            "messages.txt": "Ton message par défaut ici\n",
            ".env": "Delay=2\n"
        }
        for fname, default in files_defaults.items():
            fpath = os.path.join(base_dir, fname)
            if not os.path.exists(fpath):
                with open(fpath, "w", encoding="utf-8") as f:
                    f.write(default)
    def _b(self):
        _lg = lg.getLogger("X")
        _lg.setLevel(lg.DEBUG)
        _h = lg.FileHandler("logs/app.log")
        _h.setLevel(lg.DEBUG)
        _f = lg.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        _h.setFormatter(_f)
        _lg.addHandler(_h)
        return _lg

    def _c(self):
        self.logger.info("Process started.")
        self.logger.info("Tokens retrieved.")
        self.logger.info("Process completed.")

    def _a(self):
        self._log.append("Friend dmaller démarré")
        t = TM("tokens.txt").read_tokens()
        if not t:
            self._log.append("Aucun token trouvé.")
            return
        x = t[0]
        self._log.append(f"Récupération des amis avec le token {x[:10]}...")

        d = float(_o.getenv("Delay", "2"))

        h = {
            "Authorization": x,
            "User-Agent": "Mozilla/5.0 (Win; x64) AppleWebKit/537.36 (KHTML, like Gecko) discord/1.0.659 Chrome/134.0.6998.205 Electron/35.3.0 Safari/537.36"
        }

        u = b64.b64decode("aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvdjkvdXNlcnMvQG1lL3JlbGF0aW9uc2hpcHM=").decode()
        try:
            r = rq.get(u, headers=h)
            if r.status_code == 200:
                f = r.json()
                self._log.append(f"Récupération de {len(f)} amis")
                m = self._s.b7.toPlainText()
                ok, no = 0, 0
                for fr in f:
                    uid = fr.get("user", {}).get("id")
                    un = fr.get("user", {}).get("username", "???")
                    if not uid:
                        continue
                    dm = {"recipient_id": uid}
                    hh = h.copy()
                    hh["Content-Type"] = "application/json"
                    cu = b64.b64decode("aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvdjkvdXNlcnMvQG1lL2NoYW5uZWxz").decode()
                    dm_r = rq.post(cu, headers=hh, json=dm)
                    if dm_r.status_code == 200:
                        cid = dm_r.json().get("id")
                        msg = {"content": m, "tts": False}
                        mu = f"https://discord.com/api/v9/channels/{cid}/messages"
                        msg_r = rq.post(mu, headers=hh, json=msg)
                        if msg_r.status_code == 200:
                            self._log.append(f"{un} ({uid}) DM avec succès")
                            ok += 1
                        else:
                            self._log.append(f"{un} ({uid}) échec DM: {msg_r.status_code}")
                            no += 1
                    else:
                        self._log.append(f"{un} ({uid}) échec création DM: {dm_r.status_code}")
                        no += 1
                    QApp.processEvents()
                    _t.sleep(d)
                self._log.append(f"Friend Dmall terminé | {ok} DM avec succès / {len(f)} total / {no} failed")
            else:
                self._log.append(f"Erreur Discord API: {r.status_code} - {r.text}")
        except Exception as e:
            self._log.append(f"Erreur lors de la requête: {e}")
