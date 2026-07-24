import Sidebar from "../components/Sidebar";
import Navbar from "../components/Navbar";

export default function MainLayout({children}) {

    return (

        <div className="container">

            <Sidebar/>

            <main className="content">

                <Navbar/>

                <div className="page">

                    {children}

                </div>

            </main>

        </div>

    );

}