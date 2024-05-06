from flask import Flask, jsonify
import pandas as pd
from conectors import conectar

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h1>Bem-vindo à API de análise de vendas</h1>
    <p>Para acessar os endpoints, utilize os seguintes caminhos:</p>
    <ul>
        <li><a href="/vendas_por_produto">/vendas_por_produto</a></li>
        <li><a href="/devolucao_produto">/devolucao_produto</a></li>
        <li><a href="/all_dataset">/all_dataset</a></li>
    </ul>
    """



@app.route('/vendas_por_produto')
def vendas_por_produto():
    conn = conectar()
    if conn:
        query = """ 
        SELECT 
        ProductName, 
        FORMAT(SUM(SalesQuantity), '#,0') AS TotalVendas
        FROM 
            [dbo].[FactSales] V
        INNER JOIN 
            [dbo].[DimProduct] P ON V.ProductKey = P.ProductKey
        GROUP BY 
            ProductName
        ORDER BY 
            TotalVendas DESC;
        """
        df = pd.read_sql(query, conn)
        conn.close() 
        return jsonify(df.to_dict(orient="records"))
    else:
        return "Erro ao conectar ao banco de dados."

@app.route("/devolucao_produto")
def devolucao():
    conn = conectar()
    if conn:
        query = """ 
            SELECT 
                Manufacturer, 
                FORMAT(SUM(SalesQuantity), '#,0') AS TotalVendas, 
                FORMAT(SUM(ReturnQuantity), '#,0') AS TotalDevolucoes
            FROM 
                [dbo].[FactSales] V
            INNER JOIN 
                [dbo].[DimProduct] P ON V.ProductKey = P.ProductKey
            GROUP BY 
                Manufacturer
            ORDER BY 
                TotalVendas DESC, TotalDevolucoes DESC;
        """
        df = pd.read_sql(query, conn)
        conn.close() 
        return jsonify(df.to_dict(orient="records"))
    else:
        return "Erro ao conectar ao banco de dados."
    

@app.route("/all_dataset")
def all_data_set():
    conn = conectar() 
    if conn:
        query = """ 
            SELECT TOP 1000
                V.UnitCost AS CustoUnitario,
                V.UnitPrice AS PrecoUnitario,
                V.SalesQuantity AS QuantidadeVendida,
                V.ReturnQuantity AS QuantidadeDevolvida,
                V.ReturnAmount AS ValorDevolvido,
                V.DiscountQuantity AS QuantidadeDesconto,
                V.DiscountAmount AS ValorDesconto,
                P.ProductName AS NomeProduto,
                P.ProductDescription AS DescricaoProduto,
                P.Manufacturer AS Fabricante,
                P.BrandName AS NomeMarca,
                P.ClassName AS NomeClasse,
                P.StyleName AS NomeEstilo,
                P.ColorName AS NomeCor,
                P.Size AS Tamanho,
                P.SizeRange AS FaixaTamanho,
                P.Weight AS Peso,
                P.UnitOfMeasureName AS NomeUnidadeMedida,
                P.StockTypeName AS NomeTipoEstoque,
                P.AvailableForSaleDate AS DataDisponivelVendaProduto,
                P.Status AS StatusProduto
            FROM [dbo].[FactSales] V
            INNER JOIN [dbo].[DimProduct] P ON V.ProductKey = P.ProductKey
        """
        df = pd.read_sql(query, conn)
        conn.close()  # Fechar a conexão

        # Converter DataFrame para JSON e retornar
        return jsonify(df.to_dict(orient="records"))
    else:
        return "Erro ao conectar ao banco de dados."

@app.route('/<marca>')
def marca(marca):
    conn = conectar() 
    if conn:
        query = f""" 
            SELECT TOP 1000
                V.UnitCost AS CustoUnitario,
                V.UnitPrice AS PrecoUnitario,
                V.SalesQuantity AS QuantidadeVendida,
                V.ReturnQuantity AS QuantidadeDevolvida,
                V.ReturnAmount AS ValorDevolvido,
                V.DiscountQuantity AS QuantidadeDesconto,
                V.DiscountAmount AS ValorDesconto,
                P.ProductName AS NomeProduto,
                P.ProductDescription AS DescricaoProduto,
                P.Manufacturer AS Fabricante,
                P.BrandName AS NomeMarca,
                P.ClassName AS NomeClasse,
                P.StyleName AS NomeEstilo,
                P.ColorName AS NomeCor,
                P.Size AS Tamanho,
                P.SizeRange AS FaixaTamanho,
                P.Weight AS Peso,
                P.UnitOfMeasureName AS NomeUnidadeMedida,
                P.StockTypeName AS NomeTipoEstoque,
                P.AvailableForSaleDate AS DataDisponivelVendaProduto,
                P.Status AS StatusProduto
            FROM [dbo].[FactSales] V
            INNER JOIN [dbo].[DimProduct] P ON V.ProductKey = P.ProductKey
            Where P.BrandName  = '{marca}'
        """
        df = pd.read_sql(query, conn)
        conn.close()  # Fechar a conexão

        # Converter DataFrame para JSON e retornar
        return jsonify(df.to_dict(orient="records"))
    else:
        return "Erro ao conectar ao banco de dados."



if __name__ == "__main__":
    app.run('0.0.0.0')
