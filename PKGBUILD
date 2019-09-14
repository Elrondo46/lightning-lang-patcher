# Maintainer: Elrondo46 TuxnVape <elrond94@hotmail.com>

pkgname=lightning-lang-patcher
pkgver=1.3
pkgrel=1
pkgdesc="Patch langs of Lightning thunderbird addon"
arch=('x86_64')
license=('GPL3')
url="https://www.tuxnvape.fr/"
depends=('python' 'python-gobject' 'thunderbird')
source=("lighttrans.py"
        "llp.png"
        "llp.desktop"
        "title.png"
		"transl.glade"
		"config.json"
	"org.tnv.llp.policy")

sha256sums=('4560179d25cf8f75c4949b9033f04d670357d05f0f896baf594f0b64dfd9abd4'
            '3f1872a4ec5107ab898fac0badb414db06f53a0dfb8899daf253d26586b09264'
            '0c9e8f21252647a45b6de3ec216d5bff026ebf5400399194ceb925e749217ab2'
            'a1f6a9f35b9611ee79b122ca96ca5eeb31db275297274f03a3102d2850a65823'
            'e79927c934f404768ce6fafef848042b3457d83c7f2bad5a02922773524c1b27'
            '7d878beed054403328582ca28f41c4a4a0ce28f204c97a1ae0f132ed0c55f274'
            '583ae2438c7be9264c400098dd6df7657dc9ae41667893084bc025edb89930c6')

package() {
        install -Dm644 "llp.desktop" "${pkgdir}/usr/share/applications/llp.desktop"
        install -Dm644 "lighttrans.py" "${pkgdir}/opt/lighttrans/lighttrans.py"
        install -Dm644 "llp.png" "${pkgdir}/usr/share/icons/llp.png"
        install -Dm644 "title.png" "${pkgdir}/opt/lighttrans/title.png"
        install -Dm644 "org.tnv.llp.policy" "${pkgdir}/usr/share/polkit-1/actions/org.tnv.llp.policy"
		install -Dm644 "transl.glade" "${pkgdir}/opt/lighttrans/transl.glade"
		install -Dm644 "config.json" "${pkgdir}/opt/lighttrans/config.json"
		install -Dm644 "llp.png" "${pkgdir}/opt/lighttrans/llp.png"
} 

