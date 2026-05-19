from database.DB_connect import DBConnect
from model.artista import Artista
from model.genere import Genere


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getAllGen():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary = True)
        generi = []
        query = """select *
                from genre"""
        cursor.execute(query,)
        for row in cursor:
            generi.append(Genere(**row))

        cursor.close()
        cnx.close()
        return generi

    @staticmethod
    def getArtisti(genere):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        artisti = []
        query = """select a.ArtistId, a.Name
            from artist a, track t, album al
            where a.ArtistId = al.ArtistId and t.AlbumId = al.AlbumId and t.GenreId = %s
            group by a.ArtistId, a.Name"""
        cursor.execute(query, (genere.GenreId,))

        for row in cursor:
            artisti.append(Artista(**row))
        cursor.close()
        cnx.close()
        return artisti

    @staticmethod
    def edges(mappa, genere):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        archi = []
        query = """select a.ArtistId as ArtistId1, a2.ArtistId as ArtistId2
                from customer c, invoice i, invoiceline il, customer c2, invoice i2, invoiceline il2, track t, track t2, album a, album a2 
                where c.CustomerId = i.CustomerId and i.InvoiceId = il.InvoiceId and il.TrackId = t.trackId and t.AlbumId = a.AlbumId and 
                c2.CustomerId = i2.CustomerId and i2.InvoiceId = il2.InvoiceId and il2.TrackId = t2.trackId and t2.AlbumId = a2.AlbumId and a.ArtistId <> a2.ArtistId and c.CustomerId = c2.CustomerId 
                AND a.ArtistId < a2.ArtistId and t.GenreId = %s AND t2.GenreId = %s
                group by a.ArtistId, a2.ArtistId"""
        cursor.execute(query, (genere.GenreId, genere.GenreId,))

        for row in cursor:
            if row["ArtistId1"] in mappa and row["ArtistId2"] in mappa: #IMPORTANTE
                archi.append((mappa[row["ArtistId1"]], mappa[row["ArtistId2"]]))
        cursor.close()
        cnx.close()
        return archi

    @staticmethod
    def getAllP(mappa):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        try:
            query = """select a.ArtistId, sum(il.quantity) as q
                        from invoiceline il, track t, album a
                        where il.TrackId = t.trackId and t.AlbumId = a.AlbumId
                        group by a.ArtistId"""
            cursor.execute(query)
            result = {}
            for row in cursor:
                if row["ArtistId"] in mappa:
                    result[row["ArtistId"]] = row["q"]
            return result
        finally:
            cursor.close()
            cnx.close()
        query = """select a.ArtistId, sum(il.quantity) as q
                from invoiceline il, track t, album a
                where il.TrackId = t.trackId and t.AlbumId = a.AlbumId and a.ArtistId = %s
                group by a.ArtistId"""
        #cursor.execute(query, (artista.ArtistId,))
        #val = cursor.fetchone()
        #cursor.close()
        #cnx.close()
        #return val["q"]
